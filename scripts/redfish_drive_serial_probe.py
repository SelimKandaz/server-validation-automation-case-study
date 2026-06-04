# -*- coding: utf-8 -*-
"""
bmc_drive_serial_test.py

Purpose:
    - BMC (Redfish) üzerinden sadece disk / drive seri numaralarını deneme amaçlı çekmek.
    - Supermicro BMC dahil tüm Redfish destekli BMC'lerde çalışmayı hedefler.

Usage:
    python bmc_drive_serial_test.py
    -> IP, kullanıcı adı ve parolayı sorar.
"""

import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def redfish_get(ip, path, auth, timeout=15):
    """Simple Redfish GET helper."""
    if path.startswith("http"):
        url = path
    else:
        url = f"https://{ip}{path}"
    try:
        r = requests.get(url, auth=auth, verify=False, timeout=timeout)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        print(f"[ERROR] {url} okunamadı: {e}")
        return {}


def first_member_path(collection):
    if not collection:
        return None
    members = collection.get("Members") or []
    if not members:
        return None
    return members[0].get("@odata.id")


def discover_system_path(ip, auth):
    root = redfish_get(ip, "/redfish/v1/Systems", auth)
    sys_path = first_member_path(root) or "/redfish/v1/Systems/System.Embedded.1"
    print(f"[INFO] System path: {sys_path}")
    return sys_path


def collect_drive_serials(ip, user, password):
    auth = (user, password)
    sys_path = discover_system_path(ip, auth)

    system = redfish_get(ip, sys_path, auth)
    if not system:
        print("[ERROR] System verisi boş, devam edilemiyor.")
        return []

    storage_link = ((system.get("Storage") or {}).get("@odata.id")
                    or f"{sys_path}/Storage")
    print(f"[INFO] Storage collection: {storage_link}")

    storage_coll = redfish_get(ip, storage_link, auth)
    drives_out = []

    for m in storage_coll.get("Members", []):
        s_path = m.get("@odata.id")
        if not s_path:
            continue
        stor = redfish_get(ip, s_path, auth)
        if not stor:
            continue

        print(f"[INFO] Storage member: {s_path}  Model={stor.get('Model')} Name={stor.get('Name')}")

        for dref in stor.get("Drives", []):
            d_path = dref.get("@odata.id")
            if not d_path:
                continue
            d = redfish_get(ip, d_path, auth)
            if not d:
                continue

            # Temel alanlar
            name = d.get("Name") or d.get("Id")
            model = d.get("Model")
            media = d.get("MediaType")
            proto = d.get("Protocol")
            cap_bytes = d.get("CapacityBytes") or 0
            cap_gib = round(cap_bytes / (1024 ** 3), 2) if cap_bytes else None

            # Seri numarası bulma denemeleri
            sn = d.get("SerialNumber")

            # Bazı vendorlar SerialNumber yerine Identifiers kullanıyor
            if not sn:
                for ident in d.get("Identifiers", []) or []:
                    if isinstance(ident, dict):
                        fmt = (ident.get("DurableNameFormat") or "").lower()
                        if "serial" in fmt or "sn" in fmt:
                            sn = ident.get("DurableName")
                            if sn:
                                break

            # Oem alanını da tarayalım
            if not sn:
                oem = d.get("Oem") or {}
                for v in oem.values():
                    if isinstance(v, dict):
                        for k2, v2 in v.items():
                            if isinstance(v2, str) and "serial" in k2.lower():
                                sn = v2
                                break
                    if sn:
                        break

            drives_out.append({
                "Location": name,
                "Model": model,
                "MediaType": media,
                "Protocol": proto,
                "CapacityGiB": cap_gib,
                "SerialNumber": sn,
                "Raw": d,
            })

    return drives_out


def main():
    print("=== BMC Drive Serial Test (Redfish) ===")
    ip = input("BMC IP adresi: ").strip()
    user = input("Kullanıcı adı: ").strip()
    password = input("Parola: ").strip()

    if not ip or not user:
        print("IP ve kullanıcı adı zorunlu.")
        input("Çıkmak için Enter...")
        return

    drives = collect_drive_serials(ip, user, password)
    if not drives:
        print("\nHiç drive bilgisi alınamadı.")
        input("Çıkmak için Enter...")
        return

    print("\n=== DRIVE LİSTESİ ===")
    for d in drives:
        loc = d["Location"]
        model = d["Model"] or ""
        media = d["MediaType"] or ""
        proto = d["Protocol"] or ""
        cap = d["CapacityGiB"]
        sn = d["SerialNumber"] or "(SERIAL YOK)"
        cap_str = f"{cap} GiB" if cap is not None else "N/A"
        print(f"- {loc}: {model} | {media} {proto} | {cap_str} | SN = {sn}")

    print("\nToplam drive sayısı:", len(drives))
    input("\nBitirildi. Kapatmak için Enter'a basın...")


if __name__ == "__main__":
    main()
