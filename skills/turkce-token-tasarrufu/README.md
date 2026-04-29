# Türkçe Token Tasarrufu Skill

Türkçe Claude Code oturumlarında token tüketimini ~%40-50 düşüren bir skill.

## Nasıl çalışır

Hibrit dil stratejisi uygular:

- **İngilizce**: Kod, yorumlar, commit mesajları, log/debug, planlama, tool açıklamaları, dosya/değişken isimleri
- **Türkçe**: Sadece kullanıcıya yönelik özet, soru, sohbet

Türkçe'nin sondan eklemeli yapısı ve `ğçşıöü` gibi non-ASCII karakterleri tokenizer'da fazla token tüketiyor. İçeride İngilizce kalmak ciddi tasarruf sağlıyor; dışarısı Türkçe kaldığı için kullanıcı deneyimi de korunuyor.

## Kurulum

Bu skill, [`skill-lab-hub`](https://github.com/sdfkr22/skill-lab-hub) plugin marketplace'i içinde dağıtılıyor. Claude Code'da:

```
/plugin marketplace add sdfkr22/skill-lab-hub
/plugin install pack@skill-lab-hub
/reload-plugins
```

Sonra Türkçe yazmaya başla — skill otomatik devreye girer (`pack:turkce-token-tasarrufu`).

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
