#!/usr/bin/env python3
import sys
import ipaddress

def range_to_cidr(start_ip, end_ip):
    try:
        start = int(ipaddress.IPv4Address(start_ip))
        end = int(ipaddress.IPv4Address(end_ip))
    except ValueError:
        # Если это не IPv4, возможно IPv6 – пока пропускаем
        print(f"WARNING: IPv6 range {start_ip}-{end_ip} not supported automatically. Please use CIDR.", file=sys.stderr)
        return []
    if start == end:
        return [str(ipaddress.IPv4Address(start)) + "/32"]
    length = end - start + 1
    if (length & (length - 1)) == 0 and (start & (length - 1)) == 0:
        prefix = 32 - length.bit_length() + 1
        return [str(ipaddress.IPv4Network((start, prefix), strict=False))]
    else:
        # fallback: если не целая подсеть, разбиваем на отдельные /24 (если диапазон внутри одного /24)
        if start_ip.endswith(".0") and end_ip.endswith(".255"):
            net = ipaddress.IPv4Network(start_ip + "/24", strict=False)
            return [str(net)]
        else:
            print(f"WARNING: Cannot convert range {start_ip}-{end_ip} to CIDR. Skipping.", file=sys.stderr)
            return []

def main():
    input_file = "data/custom-ips.txt"
    output_file = "custom-converted.txt"
    try:
        with open(input_file, 'r') as f:
            lines = f.read().strip().splitlines()
    except FileNotFoundError:
        print("No custom-ips.txt found, skipping custom IPs.", file=sys.stderr)
        with open(output_file, 'w') as f:
            f.write("")
        return

    result = []
    for line in lines:
        line = line.strip()
        if not line:
            continue
        # Если уже есть маска (содержит /), просто добавляем как есть
        if '/' in line:
            result.append(line)
            continue
        # Если диапазон с дефисом (только IPv4 обрабатываем)
        if '-' in line:
            parts = line.split('-')
            if len(parts) != 2:
                print(f"WARNING: Invalid range format: {line}", file=sys.stderr)
                continue
            start, end = parts[0].strip(), parts[1].strip()
            cidrs = range_to_cidr(start, end)
            result.extend(cidrs)
        else:
            # Одиночный адрес – определяем IPv4 или IPv6
            try:
                ip = ipaddress.ip_address(line)
                if ip.version == 4:
                    result.append(line + "/32")
                else:
                    result.append(line + "/128")
            except ValueError:
                print(f"WARNING: Invalid IP address: {line}", file=sys.stderr)
                continue

    # Удаляем дубли и сортируем
    result = sorted(set(result))
    with open(output_file, 'w') as f:
        f.write("\n".join(result))

if __name__ == "__main__":
    main()