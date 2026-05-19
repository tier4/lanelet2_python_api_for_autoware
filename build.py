#!/usr/bin/env python3
"""
Build script for Poetry to compile C++ extensions before packaging.
Mirrors build.sh: Rosless-Lanelet2 → patch submodule → nested autoware CMake projects → install.
"""

from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path


def run_command(cmd: list[str], cwd: Path | None = None) -> str:
    """Run a shell command and check for errors."""
    print(f"Running: {' '.join(cmd)}")
    if cwd is not None:
        print(f"  cwd: {cwd}")
    result = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    if result.returncode != 0:
        if result.stdout:
            print(result.stdout, file=sys.stderr)
        if result.stderr:
            print(result.stderr, file=sys.stderr)
        raise RuntimeError(f"Command failed ({result.returncode}): {' '.join(cmd)}")
    return result.stdout


def cmake_install(
    label: str,
    source_dir: Path,
    build_dir: Path,
    install_prefix: Path,
) -> None:
    """Configure, build, and install one CMake project (build dir under build_poetry/)."""
    if not source_dir.is_dir():
        raise FileNotFoundError(f"{label}: missing source directory: {source_dir}")

    if build_dir.exists():
        shutil.rmtree(build_dir)
    build_dir.mkdir(parents=True, exist_ok=True)

    print(f"Building {label}...")
    run_command(
        [
            "cmake",
            str(source_dir),
            f"-DCMAKE_INSTALL_PREFIX={install_prefix}",
            "-DCMAKE_BUILD_TYPE=Release",
        ],
        cwd=build_dir,
    )
    run_command(["make", "-j"], cwd=build_dir)
    run_command(["make", "install"], cwd=build_dir)


def apply_autoware_patch(root_dir: Path) -> None:
    """Idempotent git apply of patches/autoware_lanelet2_extension_full.patch (same as build.sh)."""
    submodule = root_dir / "autoware_lanelet2_extension"
    patch = root_dir / "patches" / "autoware_lanelet2_extension_full.patch"
    if not patch.is_file():
        raise FileNotFoundError(f"Missing patch file: {patch}")
    if not submodule.is_dir():
        raise FileNotFoundError(f"Submodule directory missing: {submodule}")

    def git_rc(args: list[str]) -> int:
        r = subprocess.run(args, cwd=submodule, capture_output=True, text=True)
        if r.returncode != 0 and r.stderr:
            print(r.stderr, file=sys.stderr)
        return r.returncode

    rc = git_rc(["git", "apply", "--reverse", "--check", str(patch)])
    if rc == 0:
        rc_rev = git_rc(["git", "apply", "--reverse", str(patch)])
        if rc_rev != 0:
            raise RuntimeError("git apply --reverse failed after successful reverse check")

    rc_apply = git_rc(["git", "apply", str(patch)])
    if rc_apply != 0:
        raise RuntimeError("git apply failed")


def build() -> None:
    """Build all C++ targets into root_dir/install (same layout as build.sh)."""
    root_dir = Path(__file__).parent.absolute()
    install_prefix = root_dir / "install"
    bp = root_dir / "build_poetry"

    # 1) Rosless-Lanelet2
    cmake_install(
        "Rosless-Lanelet2",
        root_dir / "Rosless-Lanelet2",
        bp / "Rosless-Lanelet2",
        install_prefix,
    )

    # 2) Patch autoware submodule (paths inside submodule match build.sh)
    apply_autoware_patch(root_dir)

    # 3) autoware_lanelet2_extension (nested package under submodule)
    cmake_install(
        "autoware_lanelet2_extension",
        root_dir / "autoware_lanelet2_extension" / "autoware_lanelet2_extension",
        bp / "autoware_lanelet2_extension",
        install_prefix,
    )

    # 4) autoware_lanelet2_extension_python
    cmake_install(
        "autoware_lanelet2_extension_python",
        root_dir / "autoware_lanelet2_extension" / "autoware_lanelet2_extension_python",
        bp / "autoware_lanelet2_extension_python",
        install_prefix,
    )

    print("C++ extensions built successfully!")
    copy_extensions(root_dir)


def copy_extensions(root_dir: Path) -> None:
    """Copy built C++ extensions into the package tree for Poetry packaging."""
    install_dir = root_dir / "install"
    src_dir = (
        root_dir
        / "autoware_lanelet2_extension"
        / "autoware_lanelet2_extension_python"
        / "autoware_lanelet2_extension_python"
    )

    # Copy autoware extension .so files
    autoware_install = (
        install_dir
        / "lib"
        / "python3"
        / "dist-packages"
        / "autoware_lanelet2_extension_python"
    )
    if autoware_install.exists():
        src_dir.mkdir(parents=True, exist_ok=True)
        for so_file in autoware_install.glob("*.so"):
            dst = src_dir / so_file.name
            print(f"Copying {so_file} -> {dst}")
            shutil.copy2(so_file, dst)

    # Copy lanelet2 module
    lanelet2_install = install_dir / "lib" / "python3" / "dist-packages" / "lanelet2"
    lanelet2_dst = root_dir / "lanelet2"
    if lanelet2_install.exists():
        if lanelet2_dst.exists():
            shutil.rmtree(lanelet2_dst)
        print(f"Copying {lanelet2_install} -> {lanelet2_dst}")
        shutil.copytree(lanelet2_install, lanelet2_dst)

        lib_src = install_dir / "lib"
        lib_dst = lanelet2_dst / "lib"
        lib_dst.mkdir(exist_ok=True)
        for so_file in lib_src.glob("*.so*"):
            if so_file.is_file():
                print(f"Copying {so_file} -> {lib_dst / so_file.name}")
                shutil.copy2(so_file, lib_dst)


if __name__ == "__main__":
    build()
