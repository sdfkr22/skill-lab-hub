#!/usr/bin/env python3
"""
Türkçe vs İngilizce token sayısını karşılaştıran script.

Kullanım:
    python token_check.py "Türkçe metin" "English text"
    python token_check.py --file dosya.txt
    python token_check.py --file dosya.txt --english-file english.txt

İki tokenizer destekler:
  1. tiktoken (varsayılan) — yerel, hızlı, GPT-4 tokenizer'ı
     pip install tiktoken
  2. anthropic API count_tokens — Claude'un kendi tokenizer'ı
     pip install anthropic
     ANTHROPIC_API_KEY ortam değişkeni gerekir
     Kullanım: --tokenizer anthropic
"""

import argparse
import os
import sys


def count_tiktoken(text: str) -> int:
    """tiktoken (cl100k_base) ile token sayısı."""
    try:
        import tiktoken
    except ImportError:
        sys.exit("tiktoken kurulu değil. Çalıştır: pip install tiktoken")
    enc = tiktoken.get_encoding("cl100k_base")
    return len(enc.encode(text))


def count_heuristic(text: str) -> int:
    """
    Kaba, paket gerektirmeyen tahmin. Gerçek tokenizer'ın yerini tutmaz.
    İngilizce için ~4 char/token, Türkçe gibi non-ASCII ağırlıklı diller
    için ~2 char/token oranını yaklaşık modeller. Hızlı bir gösterge için.
    """
    if not text:
        return 0
    non_ascii = sum(1 for c in text if ord(c) > 127)
    ratio = non_ascii / len(text)
    chars_per_token = 4 - 2 * ratio
    return max(1, int(len(text) / chars_per_token))


def count_anthropic(text: str) -> int:
    """Anthropic API'nin count_tokens endpoint'i ile gerçek Claude token sayısı."""
    try:
        from anthropic import Anthropic
    except ImportError:
        sys.exit("anthropic kurulu değil. Çalıştır: pip install anthropic")
    if not os.environ.get("ANTHROPIC_API_KEY"):
        sys.exit("ANTHROPIC_API_KEY ortam değişkeni gerekli.")
    client = Anthropic()
    result = client.messages.count_tokens(
        model="claude-sonnet-4-5",
        messages=[{"role": "user", "content": text}],
    )
    return result.input_tokens


def report(label: str, text: str, count_fn) -> int:
    tokens = count_fn(text)
    chars = len(text)
    ratio = tokens / chars if chars else 0
    preview = text if len(text) <= 60 else text[:57] + "..."
    print(f"  [{label}]")
    print(f"    Önizleme: {preview!r}")
    print(f"    Karakter: {chars}")
    print(f"    Token:    {tokens}")
    print(f"    Token/karakter: {ratio:.3f}")
    return tokens


def main():
    parser = argparse.ArgumentParser(
        description="Türkçe vs İngilizce token sayısını karşılaştır."
    )
    parser.add_argument("turkish", nargs="?", help="Türkçe metin")
    parser.add_argument("english", nargs="?", help="İngilizce metin (opsiyonel)")
    parser.add_argument("--file", help="Türkçe metin dosyası")
    parser.add_argument("--english-file", help="İngilizce metin dosyası")
    parser.add_argument(
        "--tokenizer",
        choices=["tiktoken", "anthropic", "heuristic"],
        default="tiktoken",
        help=(
            "Hangi tokenizer kullanılsın. "
            "tiktoken: yerel, GPT-4 tokenizer (varsayılan, pip install tiktoken). "
            "anthropic: Claude API (kesin sayı, ANTHROPIC_API_KEY gerekir). "
            "heuristic: paket gerekmez, kaba tahmin."
        ),
    )
    args = parser.parse_args()

    # Türkçe içeriği al
    if args.file:
        with open(args.file, encoding="utf-8") as f:
            turkish = f.read()
    elif args.turkish:
        turkish = args.turkish
    else:
        parser.error("Türkçe metin veya --file gerekli.")

    # İngilizce içeriği al (varsa)
    english = None
    if args.english_file:
        with open(args.english_file, encoding="utf-8") as f:
            english = f.read()
    elif args.english:
        english = args.english

    counters = {
        "tiktoken": count_tiktoken,
        "anthropic": count_anthropic,
        "heuristic": count_heuristic,
    }
    count_fn = counters[args.tokenizer]
    print(f"Tokenizer: {args.tokenizer}")
    print()

    tr_tokens = report("Türkçe", turkish, count_fn)

    if english is not None:
        print()
        en_tokens = report("İngilizce", english, count_fn)
        print()
        print("--- Karşılaştırma ---")
        if en_tokens:
            overhead = (tr_tokens - en_tokens) / en_tokens * 100
            print(f"Türkçe / İngilizce token oranı: {tr_tokens / en_tokens:.2f}x")
            print(f"Türkçe overhead: %{overhead:+.1f}")
            if overhead > 0:
                saving = (tr_tokens - en_tokens) / tr_tokens * 100
                print(
                    f"İngilizce'ye geçince tasarruf: %{saving:.1f} "
                    f"({tr_tokens - en_tokens} token)"
                )


if __name__ == "__main__":
    main()
