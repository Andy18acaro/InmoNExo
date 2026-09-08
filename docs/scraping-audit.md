# Scraping audit — InmoNExo seed Developers

Audit date: **2026-09-08**. Primary sources only (live HTML/headers via curl + page fetch). No invented catalogs or prices.

## Methodology

For each Developer: homepage, project listing (if any), ≥1 project detail, `robots.txt`, sitemap index when reachable. Tech notes from headers and asset paths (`wp-content`, generators, CDN). Field tables mark what is **publicly visible**; missing = not shown (do not invent). Calendar `delivery_date` was **not** found as an explicit date on audited pages (only stage labels).

---

## UNIO Grupo Inmobiliario

- **Website:** https://unio.pe/ (https://unio.pe/inicio/ same content)
- **Technology observations:** WordPress (Link `wp-json`, PHP 8.4, Hostinger/hcdn, LiteSpeed). Hello Elementor + Elementor + JetEngine / JetMenu / Jet Smart Filters. Rank Math. CPT `proyectos` / `unidades` in REST.
- **Project listing URL:** https://unio.pe/proyectos-venta/ (also `/proyectos-entregados/`)
- **Project detail URL pattern:** `https://unio.pe/proyectos/{slug}/` (e.g. `varenna-san-isidro`). Homepage names Amalfi / Altezza / Lucca but matching detail URLs returned **404** in audit. Sitemap lists only Varenna.
- **Static vs Dynamic:** Mostly server-rendered Elementor HTML.
- **Recommended extraction method:** Requests + BeautifulSoup (Playwright only for interactive tipología widgets).
- **Fields available publicly:**

| Field | Public? | Notes |
|-------|---------|-------|
| project_name | Yes | Varenna on listing/detail; other names on home only |
| district | Yes | San Isidro (Varenna); home labels for others |
| city | Implied | Lima |
| address | Partial | e.g. Calle Los Cisnes (incomplete formal address) |
| status | Partial | REST taxonomy; thinner marketing stages |
| price_min | **No** | Via asesor only |
| currency | N/A | |
| area_m2 | Yes | Desde 70–213 m² |
| bedrooms | Yes | 2–3 dorms / tipologías |
| delivery_date | **No** | |
| units | Yes | Boutique 13 depas; disponibilidad codes |

- **Potential challenges:** Tiny live catalog; prices gated; REST thin vs Elementor HTML; robots allow except `/wp-admin/`.
- **Sources:** https://unio.pe/, https://unio.pe/inicio/, https://unio.pe/robots.txt, https://unio.pe/sitemap_index.xml, https://unio.pe/proyectos-sitemap.xml, https://unio.pe/proyectos-venta/, https://unio.pe/proyectos/varenna-san-isidro/, https://unio.pe/wp-json/wp/v2/types, https://unio.pe/wp-json/wp/v2/proyectos?per_page=20

---

## Grupo MG

- **Website:** https://grupomg.pe/
- **Technology observations:** WordPress theme `wp-grupo-mg` (Staff Digital). WP Rocket lazyload. jQuery/Owl/Fancybox. Rank Math. Apache. **WP REST blocked** by iThemes Security (401).
- **Project listing URL:** https://grupomg.pe/departamentos-en-venta/en-venta/ (district filters; `/departamentos-en-venta/entregado/`)
- **Project detail URL pattern:** `https://grupomg.pe/departamentos/{slug}/` (e.g. `/departamentos/allure/`)
- **Static vs Dynamic:** Listing cards + hero metrics in initial HTML; cotizador unit rows JS-heavy.
- **Recommended extraction method:** Requests + BeautifulSoup for listing/detail metrics; Playwright later only for cotizador.
- **Fields available publicly:**

| Field | Public? | Notes |
|-------|---------|-------|
| project_name | Yes | ALLURE, HUIRACOCHA, LURENT, … |
| district | Yes | Jesús María, Magdalena, Pueblo Libre, San Borja, San Miguel, Santa Beatriz, Surco, Surquillo |
| city | Implied | Lima |
| address | Yes | On cards + detail |
| status | Yes | EN CONSTRUCCIÓN, ENTREGA INMEDIATA, LANZAMIENTO, PRE VENTA |
| price_min | Yes | e.g. Allure Desde S/ 268000 |
| currency | Yes | PEN |
| area_m2 | Yes | e.g. desde 40 m2 |
| bedrooms | Partial | Form/options; not always clean on card |
| delivery_date | **No** | Stage only |
| units | Yes (detail) | e.g. Allure 148 depas |

- **Potential challenges:** `Crawl-delay: 10` in robots.txt; REST locked; noisy duplicate chrome HTML.
- **Sources:** https://grupomg.pe/, https://grupomg.pe/robots.txt, https://grupomg.pe/departamentos-en-venta/en-venta/, https://grupomg.pe/departamentos/allure/, https://grupomg.pe/wp-json/wp/v2/types (401)

---

## Albamar

- **Website:** https://albamar.com.pe/
- **Technology observations:** WordPress `albamar-wp` (Staff Digital family). Cloudflare + email obfuscation. Rank Math. WP Rocket. CF7. Sperant portal (`albamar.sperant.com`) — not public listing API.
- **Project listing URL:** https://albamar.com.pe/departamentos/
- **Project detail URL pattern:** `https://albamar.com.pe/departamentos/{slug}/` (sitemap ~25+ URLs)
- **Static vs Dynamic:** Card fields in HTML; detail mixes static + forms.
- **Recommended extraction method:** Requests + BeautifulSoup (+ sitemap discovery). Playwright if Cloudflare challenges automation.
- **Fields available publicly:**

| Field | Public? | Notes |
|-------|---------|-------|
| project_name | Yes | Detail titles / slugs |
| district | Yes | Filters + address |
| city | Implied | Lima |
| address | Yes | On cards |
| status | Yes | Entrega inmediata, En Construcción, En Lanzamiento, … |
| price_min | Yes | Listing + some detail “desde S/ …” |
| currency | Yes | PEN |
| area_m2 | Yes | |
| bedrooms | Yes | |
| delivery_date | **No** | |
| units | Not clearly | Total count inconsistent |

- **Potential challenges:** Cloudflare AI-bot disallow list; some prices with asterisks; Sperant out of scope.
- **Sources:** https://albamar.com.pe/, https://albamar.com.pe/robots.txt, https://albamar.com.pe/sitemap_index.xml, https://albamar.com.pe/departamentos-sitemap.xml, https://albamar.com.pe/departamentos/, https://albamar.com.pe/departamentos/albamar-move/, https://albamar.com.pe/wp-json/wp/v2/types

---

## HL Desarrollos (HL.DI)

- **Website:** https://hldi.pe/
- **Technology observations:** WordPress + Hello Elementor + Elementor Pro + JetEngine. Yoast. Homepage JS `ajaxProyectos` → `admin-ajax.php?action=listar_proyectos`. CPT `proyectos` in REST. Dual URLs: pretty root pages (`/sq2-work-and-living/`) and CPT (`/proyectos/{slug}/`).
- **Project listing URL:** https://hldi.pe/proyectos/ (also dense homepage cards)
- **Project detail URL pattern:** Prefer canonicalization across `/proyectos/{slug}/` and marketing root slugs.
- **Static vs Dynamic:** Listing cards with price/address/status in HTML; “mostrar más” may AJAX.
- **Recommended extraction method:** Requests + BeautifulSoup on `/` or `/proyectos/`; optional REST for IDs/slugs. Playwright only if AJAX hides rows.
- **Fields available publicly:**

| Field | Public? | Notes |
|-------|---------|-------|
| project_name | Yes | SQ 2, LLUMS, URBAN MOOD, MALENA, MILLENNIUM, … |
| district | Yes | Surquillo, Jesús María, Barranco, Magdalena, Chorrillos, Santa Catalina, Miraflores |
| city | Implied | Lima |
| address | Yes | Full street on cards |
| status | Yes | Nuevo lanzamiento, Pre venta, En construcción, Pronta entrega, Entrega inmediata |
| price_min | Yes | e.g. SQ 2 Desde S/ 292,769* |
| currency | Yes | PEN |
| area_m2 | Partial | Stronger on detail |
| bedrooms | Partial | Stronger on detail |
| delivery_date | **No** | |
| units | Not on audited cards | |

- **Potential challenges:** Dual URL drift; prices with `*`; incomplete Yoast project sitemap — do not rely on sitemap alone. robots.txt allows all (empty Disallow).
- **Sources:** https://hldi.pe/, https://hldi.pe/robots.txt, https://hldi.pe/sitemap_index.xml, https://hldi.pe/proyectos-sitemap.xml, https://hldi.pe/proyectos/, https://hldi.pe/sq2-work-and-living/, https://hldi.pe/wp-json/wp/v2/proyectos?per_page=20

---

## Morada

- **Website:** https://morada.pe/
- **Technology observations:** WordPress 6.9 + Bricks builder + Limapixel. Complianz. Rank Math. reCAPTCHA on forms.
- **Project listing URL:** https://morada.pe/proyectos/ (filters: distrito, etapa, arquitecto)
- **Project detail URL pattern:** `https://morada.pe/proyectos/{slug}/`
- **Static vs Dynamic:** Core facts in HTML; tipología/cotizar interactive.
- **Recommended extraction method:** Requests + BeautifulSoup.
- **Fields available publicly:**

| Field | Public? | Notes |
|-------|---------|-------|
| project_name | Yes | Street-style names |
| district | Yes | Miraflores, San Isidro, Barranco, … |
| city | Implied | Lima |
| address | Partial | Name ≈ address; Maps links |
| status | Yes | Lanzamiento, En construcción, Entrega inmediata |
| price_min | **No** | Gated |
| currency | N/A | |
| area_m2 | Yes | Ranges + tipologías |
| bedrooms | Yes | |
| delivery_date | **No** | |
| units | Yes (detail) | e.g. Arica 1090: 22 depas |

- **Potential challenges:** No public prices → weak for price intelligence until other signals or later access.
- **Sources:** https://morada.pe/, https://morada.pe/proyectos/, https://morada.pe/proyectos/arica-1090/, https://morada.pe/robots.txt, https://morada.pe/sitemap_index.xml, https://morada.pe/proyectos-sitemap.xml

---

## Comparison — first Provider for MVP

| Rank | Company | Why | Listing field density | Method | Main risk |
|------|---------|-----|----------------------|--------|-----------|
| **1** | **HL.DI** | Name + district + address + status + price_min on one page | Strong | Requests+BS | Dual URLs; weak sitemap |
| **2** | **Grupo MG** | Same density + area_m2; large catalog | Strong | Requests+BS | Crawl-delay 10; REST locked |
| **3** | **Albamar** | Price/area/beds/status; large sitemap | Strong | Requests+BS | Cloudflare |
| **4** | **Morada** | Clean structure; areas/units | Weak on price | Requests+BS | No public prices |
| **5** | **UNIO** | Deep unit detail on one Project | Thin catalog | Requests+BS | Prices gated |

**Decision (post-audit):** first vertical-slice Provider = **HL.DI**, then Grupo MG, then Albamar, then Morada/UNIO (expect null Money where gated).

Raw HTML snapshots used during audit live under `E:\DEV\projects\_scraping_audit_tmp` (local scratch; not committed).
