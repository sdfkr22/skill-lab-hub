---
name: turkce-token-tasarrufu
description: Türkçe Claude Code oturumlarında token tüketimini ~%40-50 düşüren hibrit dil stratejisi. Türkçe karakterler (çğıöşü) ve sondan eklemeli yapı tokenizer'da ciddi overhead yaratır; bu skill Claude'un iç çalışmasını (kod, yorumlar, commit, log, plan, tool description, dosya/değişken isimleri) İngilizce yapmasını sağlar, sadece kullanıcıya yönelik özet/soru/sohbet Türkçe kalır. Kullanıcı Türkçe yazdığında otomatik tetiklenir. Ayrıca "token tasarrufu", "Türkçe optimizasyon", "context dolduruyor", "limitim doluyor", "context window" gibi ifadelerde de devreye gir. Kullanıcı açıkça "her şey Türkçe olsun" demediği sürece Türkçe oturumlarda bu skill aktif olmalı. Mevcut kod tabanı Türkçe yorumlu ise stiline uyum öncelikli.
---

# Türkçe Token Tasarrufu

Türkçe BPE tokenizer'da ~2x token tüketir. Bu skill içerideki teknik içeriği İngilizce, dışarıdaki sohbeti Türkçe tutarak ~%40-50 tasarruf sağlar.

## Kural: İçeride İngilizce, dışarıda Türkçe

### İngilizce yap

Kullanıcı Türkçe yazsa bile şu öğeler İngilizce:

- Kod yorumları, değişken/fonksiyon/dosya/branch isimleri
- Commit mesajları ve PR description'ları
- Log/debug/error string'leri, test isimleri
- Tool çağrılarındaki `description` parametresi (örn: "Reading auth.ts" — "auth.ts dosyasını okuyorum" değil)
- TodoWrite görevleri ve iç planlama
- README ve doküman (kullanıcı özel olarak Türkçe istemediyse)

### Türkçe kalsın

Sadece kullanıcıyla doğrudan konuşma:

- Sorular, onay istekleri, özetler, sonuç açıklamaları
- Hata raporları (kullanıcıya yönelik)
- Kısa onaylar

## Ek tasarruf kuralları

1. **Process narration yapma.** "Şimdi şunu açıp şuna bakıp..." yerine sadece yap, sonunda özetle.
2. **Dolgu cümlesi yok.** "Anladım, hemen başlıyorum" yazma. Direkt işe geç.
3. **Soruyu tekrar etme.** "Sen şunu sordun..." gibi giriş yapma.
4. **Liste yerine düz cümle** — kısa cevaplarda madde işareti token israfı.
5. **Kod bloğu içinde Türkçe açıklama yazma.** Açıklama bloktan önce/sonra ayrı cümle olarak.
6. **Cevabı tekrar tekrar onaylatma.** Tek soru sor, gereksiz "doğru anladım mı?" turlarına girme.

## Uygulama

Skill ilk devreye girdiğinde kullanıcıya tek cümle bildir:

> "Token tasarrufu için hibrit mod: kod İngilizce, sohbet Türkçe. Tümü Türkçe istersen söyle."

Sonra sessizce uygula, her cevapta hatırlatma.

## İstisnalar

Şu durumlarda hibrit modu bırak ve her şeyi Türkçe yap:

- Kullanıcı "her şey Türkçe olsun" / "yorumları da Türkçe yaz" derse
- Kullanıcı Türkçe öğretici/dokümantasyon yazıyorsa
- **Mevcut kod tabanı Türkçe yorumlu/Türkçe değişken isimli ise** — tutarlılık her şeyin üstünde

## Ölçüm

Etkisini ölçmek için `scripts/token_check.py`:

```bash
# Karşılaştırma
python scripts/token_check.py "Merhaba dünya" "Hello world"

# Dosya
python scripts/token_check.py --file ornek.txt
```

Üç tokenizer modu: `--tokenizer heuristic` (paket gerekmez), varsayılan `tiktoken`, `--tokenizer anthropic` (gerçek Claude sayısı, API key gerekir).
