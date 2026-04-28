# Türkçe Token Tasarrufu Skill

Türkçe Claude Code oturumlarında token tüketimini ~%40-50 düşüren bir skill.

## Nasıl çalışır

Hibrit dil stratejisi uygular:

- **İngilizce**: Kod, yorumlar, commit mesajları, log/debug, planlama, tool açıklamaları, dosya/değişken isimleri
- **Türkçe**: Sadece kullanıcıya yönelik özet, soru, sohbet

Türkçe'nin sondan eklemeli yapısı ve `ğçşıöü` gibi non-ASCII karakterleri tokenizer'da fazla token tüketiyor. İçeride İngilizce kalmak ciddi tasarruf sağlıyor; dışarısı Türkçe kaldığı için kullanıcı deneyimi de korunuyor.

## Kurulum

Claude Code'da skill yüklemek için:

```bash
# Skill'leri tutan klasöre kopyala
mkdir -p ~/.claude/skills
cp -r turkce-token-tasarrufu ~/.claude/skills/
```

Sonra Claude Code'u yeniden başlat. Skill artık otomatik olarak Türkçe mesajlarda devreye girecek.

## Token ölçüm scripti

`scripts/token_check.py` Türkçe vs İngilizce token sayısını karşılaştırır.

### Bağımlılıklar

Üç tokenizer modu var, ihtiyacına göre seç:

```bash
# 1. heuristic (paket gerekmez, kaba tahmin)
python scripts/token_check.py --tokenizer heuristic "metin"

# 2. tiktoken (yerel, hızlı, GPT-4 tokenizer'ı — Claude için yaklaşık)
pip install tiktoken
python scripts/token_check.py "metin"  # varsayılan

# 3. anthropic (kesin Claude token sayısı, API çağrısı yapar)
pip install anthropic
export ANTHROPIC_API_KEY=sk-ant-...
python scripts/token_check.py --tokenizer anthropic "metin"
```

### Kullanım

```bash
# İki metni karşılaştır
python scripts/token_check.py "Merhaba dünya" "Hello world"

# Bir dosyanın token sayısı
python scripts/token_check.py --file ornek.txt

# İki dosyayı karşılaştır
python scripts/token_check.py --file tr.md --english-file en.md
```

## Hibrit modu kapatmak

Skill aktifken her şeyi Türkçe istersen Claude'a şunu söyle:

> "Her şey Türkçe olsun"

ya da

> "Yorumları da Türkçe yaz"

Skill kendiliğinden devre dışı kalır.
