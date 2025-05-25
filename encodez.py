#!/usr/bin/env python3
import urllib.parse
import base64
import argparse
from rich import print
from rich.console import Console

console = Console()

def url_encode(payload):
    return urllib.parse.quote(payload)

def double_url_encode(payload):
    return urllib.parse.quote(urllib.parse.quote(payload))

def base64_encode(payload):
    return base64.b64encode(payload.encode()).decode()

def generate_variants(payload):
    return [
        payload,
        payload.replace("../", "..%2f"),
        payload.replace("../", "%2e%2e/"),
        payload.replace("../", "..%252f"),
        payload.replace("/", "%2f"),
        payload.replace("/", "%252f"),
    ]

def encode_all(payload):
    variants = generate_variants(payload)
    results = []

    for v in variants:
        results.append({
            "raw": v,
            "url": url_encode(v),
            "double_url": double_url_encode(v),
            "base64": base64_encode(v)
        })

    return results

def main():
    parser = argparse.ArgumentParser(description="Encodex - Payload Encoding Toolkit")
    parser.add_argument("--payload", "-p", required=True, help="Payload to encode")
    parser.add_argument("--url", action="store_true", help="URL encode the payload")
    parser.add_argument("--double", action="store_true", help="Double URL encode the payload")
    parser.add_argument("--base64", action="store_true", help="Base64 encode the payload")
    parser.add_argument("--all", action="store_true", help="Apply all encodings to payload variants")
    parser.add_argument("--silent", action="store_true", help="Only print the encoded values (no labels/colors)")

    args = parser.parse_args()

    if args.all:
        all_encoded = encode_all(args.payload)
        for idx, enc in enumerate(all_encoded, start=1):
            if not args.silent:
                console.rule(f"[bold green]Variant {idx}")
                print(f"[yellow]Raw      :[/] {enc['raw']}")
                print(f"[cyan]URL      :[/] {enc['url']}")
                print(f"[cyan]Double   :[/] {enc['double_url']}")
                print(f"[magenta]Base64   :[/] {enc['base64']}\n")
            else:
                print(enc["url"])

    else:
        if args.url:
            print(url_encode(args.payload) if args.silent else f"[cyan]URL encoded:[/] {url_encode(args.payload)}")
        if args.double:
            print(double_url_encode(args.payload) if args.silent else f"[cyan]Double URL:[/] {double_url_encode(args.payload)}")
        if args.base64:
            print(base64_encode(args.payload) if args.silent else f"[magenta]Base64   :[/] {base64_encode(args.payload)}")

if __name__ == "__main__":
    main()
