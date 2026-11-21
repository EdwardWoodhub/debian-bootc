# dracut stage guard: dracut exits non-zero on explicitly --add'ed modules the
# tree does not ship (Fedora-only modules like anaconda / qemu-net on a Debian
# installer tree). Filter the stage options down to what the tree actually has,
# inject dmsquash-live when building the live installer tree, and strip
# ostree/bootc root-prep modules that break live squashfs switch-root.
import glob
import re

p = glob.glob('/usr/lib/osbuild/stages/org.osbuild.dracut')[0]
src = open(p).read()
old = "    extra = options.get(\"extra\", [])"
new = """    extra = options.get("extra", [])

    # Cross-distro guard: drop --add/-m names whose module does not exist in
    # the tree (module dirs are <nn>-<name> or <nn><name> under usr/lib/dracut/modules.d).
    _md = _os.path.join(tree, "usr/lib/dracut/modules.d")
    _have = set()
    if _os.path.isdir(_md):
        for _n in _os.listdir(_md):
            _m = _re.sub(r'^[0-9]{2}-?', '', _n).lower()
            _have.add(_m)
    _deny = {"ostree", "bootc", "biosdevname"}
    if add_modules or modules:
        add_modules = [m for m in add_modules if m.lower() in _have and m.lower() not in _deny]
        modules = [m for m in modules if m.lower() in _have and m.lower() not in _deny]
    if "dmsquash-live" in _have:
        for _lm in ("dmsquash-live", "img-lib", "rootfs-block", "dm", "overlayfs"):
            if _lm in _have and _lm not in add_modules:
                add_modules.append(_lm)
    extra = list(extra) + ["--omit", "ostree bootc", "--filesystems", "squashfs iso9660 overlay"]"""
assert old in src, 'dracut stage shape changed'
src = src.replace(old, new, 1)
src = src.replace('def main(tree, options):\n    kernels = options["kernel"]',
                  'def main(tree, options):\n    import os as _os, re as _re\n    kernels = options["kernel"]', 1)
open(p, 'w').write(src)
print('patched', p)
