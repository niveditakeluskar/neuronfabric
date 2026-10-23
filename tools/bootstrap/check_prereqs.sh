#!/usr/bin/env bash
# NeuroGuard environment preflight (TDS §E2#102, §E2.1).
#
# NON-DESTRUCTIVE: only reads tool versions and system facts. It never installs packages,
# changes settings, loads kernel objects or uses sudo. Hostname and username are NOT recorded.
#
# Usage:
#   tools/bootstrap/check_prereqs.sh                # human-readable report
#   tools/bootstrap/check_prereqs.sh --json FILE    # also write a machine-readable report
#
# Exit code: 0 always (this is a report, not a gate). Component readiness is in the output.

set -u

JSON_OUT=""
if [ "${1:-}" = "--json" ]; then
  JSON_OUT="${2:?--json requires a file path}"
fi

OS="$(uname -s)"
ARCH="$(uname -m)"
KERNEL="$(uname -r)"
if [ "$OS" = "Darwin" ]; then
  OS_NAME="macOS $(sw_vers -productVersion 2>/dev/null)"
elif [ -r /etc/os-release ]; then
  OS_NAME="$(. /etc/os-release; echo "${PRETTY_NAME:-$NAME}")"
else
  OS_NAME="$OS"
fi

json_escape() { printf '%s' "$1" | sed -e 's/\\/\\\\/g' -e 's/"/\\"/g' | tr -d '\000-\037'; }

# name | version command | components that need it
TOOLS="
git|git --version|all
python3|python3 --version|governance,analytics
docker|docker --version|brain-dev,tests
ruby|ruby --version|governance(yaml-fallback)
rustup|rustup --version|linux-agent
rustc|rustc --version|linux-agent
cargo|cargo --version|linux-agent
clang|clang --version|ebpf
llvm-config|llvm-config --version|ebpf
llvm-strip|llvm-strip --version|ebpf
bpftool|bpftool version|ebpf
pahole|pahole --version|ebpf
make|make --version|ebpf
cmake|cmake --version|ebpf
qemu-system-x86_64|qemu-system-x86_64 --version|kernel-tests
go|go version|brain,network
node|node --version|web
npm|npm --version|web
buf|buf --version|contracts
protoc|protoc --version|contracts
kas|kas --version|yocto
bitbake|bitbake --version|yocto
kubectl|kubectl version --client|kubernetes
helm|helm version --short|kubernetes
kind|kind version|kubernetes
gh|gh --version|github-verification
shellcheck|shellcheck --version|lint
yamllint|yamllint --version|lint
uv|uv --version|analytics
pandoc|pandoc --version|docs
pdftotext|pdftotext -v|docs
textutil|textutil -help|docs(macOS)
"

present_list=""
missing_list=""
tool_json=""
printf '%-20s %-9s %s\n' "TOOL" "STATUS" "VERSION / NEEDED BY"
printf '%-20s %-9s %s\n' "----" "------" "-------------------"
while IFS='|' read -r name cmd needed; do
  [ -z "$name" ] && continue
  if command -v "$name" >/dev/null 2>&1; then
    ver="$($cmd 2>&1 | head -1)"
    status="present"
    present_list="$present_list $name"
    printf '%-20s %-9s %s\n' "$name" "OK" "$ver"
  else
    ver=""
    status="missing"
    missing_list="$missing_list $name"
    printf '%-20s %-9s %s\n' "$name" "MISSING" "needed by: $needed"
  fi
  tool_json="$tool_json{\"name\":\"$(json_escape "$name")\",\"status\":\"$status\",\"version\":\"$(json_escape "$ver")\",\"needed_by\":\"$(json_escape "$needed")\"},"
done <<EOF
$TOOLS
EOF
tool_json="[${tool_json%,}]"

has() { case " $present_list " in *" $1 "*) return 0;; *) return 1;; esac; }

# Python modules used by repository tooling
pyyaml="missing"
if has python3 && python3 -c 'import yaml' >/dev/null 2>&1; then pyyaml="present"; fi

# Linux kernel facts (TDS §E2.1). Presence does not prove hook-specific attach success.
btf="n/a"; bpf_cfg="n/a"
if [ "$OS" = "Linux" ]; then
  if [ -e /sys/kernel/btf/vmlinux ]; then btf="present"; else btf="missing"; fi
  if [ -r /proc/config.gz ]; then
    bpf_cfg="$(zgrep -E '^CONFIG_(BPF|BPF_SYSCALL|DEBUG_INFO_BTF|BPF_LSM)=' /proc/config.gz 2>/dev/null | tr '\n' ' ')"
  elif [ -r "/boot/config-$KERNEL" ]; then
    bpf_cfg="$(grep -E '^CONFIG_(BPF|BPF_SYSCALL|DEBUG_INFO_BTF|BPF_LSM)=' "/boot/config-$KERNEL" | tr '\n' ' ')"
  else
    bpf_cfg="unreadable"
  fi
fi

# Component readiness. Reference host per TDS §E2: Ubuntu 24.04 LTS x86_64 (kernel/Yocto), Windows + WDK (drivers).
is_ref_linux="no"
if [ "$OS" = "Linux" ] && [ "$ARCH" = "x86_64" ] && printf '%s' "$OS_NAME" | grep -q 'Ubuntu 24.04'; then is_ref_linux="yes"; fi

verdict() { # component, condition-result(0/1), reason
  if [ "$2" -eq 0 ]; then printf 'GO'; else printf 'NO-GO'; fi
}
all_present() { for t in "$@"; do has "$t" || return 1; done; return 0; }

r_gov=1;    all_present git python3 && { [ "$pyyaml" = present ] || has ruby; } && r_gov=0
r_ebpf=1;   [ "$is_ref_linux" = yes ] && all_present clang llvm-strip bpftool pahole make && [ "$btf" = present ] && r_ebpf=0
r_agent=1;  all_present rustup cargo && r_agent=0
r_yocto=1;  [ "$is_ref_linux" = yes ] && all_present kas git python3 && r_yocto=0
r_brain=1;  all_present go docker && r_brain=0
r_contr=1;  all_present buf && r_contr=0
r_web=1;    all_present node npm && r_web=0
r_k8s=1;    all_present kubectl helm docker && r_k8s=0
r_win=1;    case "$OS" in MINGW*|MSYS*|CYGWIN*|Windows_NT) r_win=0;; esac

echo
echo "Host: $OS_NAME | $OS $KERNEL | $ARCH"
echo "Reference Linux build host (Ubuntu 24.04 x86_64): $is_ref_linux"
echo "PyYAML: $pyyaml   BTF: $btf   BPF config: $bpf_cfg"
echo
printf '%-26s %s\n' "COMPONENT" "READINESS"
printf '%-26s %s\n' "governance/docs"         "$(verdict gov $r_gov)"
printf '%-26s %s\n' "contracts (buf)"         "$(verdict contr $r_contr)"
printf '%-26s %s\n' "linux eBPF build/test"   "$(verdict ebpf $r_ebpf)  (requires reference Linux host + BTF)"
printf '%-26s %s\n' "rust agent build"        "$(verdict agent $r_agent)"
printf '%-26s %s\n' "yocto image build"       "$(verdict yocto $r_yocto)  (requires reference Linux host)"
printf '%-26s %s\n' "brain services (Go)"     "$(verdict brain $r_brain)"
printf '%-26s %s\n' "web console"             "$(verdict web $r_web)  (stack pending ADR-024)"
printf '%-26s %s\n' "kubernetes dev"          "$(verdict k8s $r_k8s)"
printf '%-26s %s\n' "windows driver build"    "$(verdict win $r_win)  (requires Windows + WDK)"
echo
echo "Missing tools:${missing_list:- none}"
echo "This script installed nothing. Install missing prerequisites only with approval."

if [ -n "$JSON_OUT" ]; then
  cat > "$JSON_OUT" <<EOF
{
  "schema_version": 1,
  "document": "environment_report",
  "generated_at_utc": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
  "generator": "tools/bootstrap/check_prereqs.sh",
  "host": {
    "os": "$(json_escape "$OS")",
    "os_name": "$(json_escape "$OS_NAME")",
    "kernel": "$(json_escape "$KERNEL")",
    "arch": "$(json_escape "$ARCH")",
    "is_reference_linux_build_host": "$is_ref_linux",
    "btf_vmlinux": "$btf",
    "bpf_kernel_config": "$(json_escape "$bpf_cfg")"
  },
  "python_modules": {"yaml": "$pyyaml"},
  "tools": $tool_json,
  "component_readiness": {
    "governance_docs": "$(verdict x $r_gov)",
    "contracts": "$(verdict x $r_contr)",
    "linux_ebpf": "$(verdict x $r_ebpf)",
    "rust_agent": "$(verdict x $r_agent)",
    "yocto": "$(verdict x $r_yocto)",
    "brain_go": "$(verdict x $r_brain)",
    "web_console": "$(verdict x $r_web)",
    "kubernetes_dev": "$(verdict x $r_k8s)",
    "windows_driver": "$(verdict x $r_win)"
  },
  "notes": "Presence of tools/config does not prove hook-specific attach success (TDS E2.1). Hostname and username intentionally omitted."
}
EOF
  echo "Wrote $JSON_OUT"
fi
exit 0
