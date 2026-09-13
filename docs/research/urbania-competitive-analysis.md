# Análisis competitivo: modelo de negocio de Urbania y referentes US

**Fecha:** 2026-09-13
**Contexto:** post-MVP de InmoNExo. Objetivo: entender el modelo de Urbania (líder en Perú), identificar plataformas US con funcionalidades comparables y extraer features/value-adds que hagan viable competir.

## 1. Modelo de negocio de Urbania

**Qué es:** portal inmobiliario líder de Perú (37,800+ propiedades, 12+ años). Lanzada por Grupo El Comercio, vendida a Navent Group junto con Aptitus; QuintoAndar (brasilero) adquirió Navent para reforzar su oferta LATAM — tiene respaldo financiero serio.

**Líneas de ingreso:**

| Línea | Detalle |
|---|---|
| Planes de publicación freemium | Packs, planes individuales y "Zona Demand" para profesionales; también planes para particulares. Es el portal "más conocido pero también el más caro" de Perú. |
| Leads y destacados | "Destacado plus" (placement premium), WhatsApp/teléfono en ficha, "Consultar precio" que esconde el precio para forzar el lead. |
| Servicios a desarrolladores | Urbania 3D (showroom virtual para proyectos en pozo con disponibilidad y precios en vivo); ferias Expo Urbania. |
| Contenido y autoridad | Guías "Urbania te explica" (SEO masivo), directorio de inmobiliarias, Urbania Índex (informe mensual del mercado de Lima: precio promedio S/6,699/m², retorno bruto 5.31%). |
| Financiamiento | Alianzas con bancos visibles en fichas de proyecto. |

**Debilidades estructurales (oportunidad de InmoNExo):**

- Sus datos de proyecto son **avisos, no datasets**: sin histórico de precios por proyecto, sin feed de eventos, sin métricas de inventario/absorción.
- Su índice es **mensual y agregado a nivel Lima** — nada por distrito, desarrollador ni proyecto.
- Su incentivo es maximizar publicación de avisos, no profundidad del dato (el hueco que ADR-0005 ya apunta).
- "Consultar precio" = precio oculto: InmoNExo ya estructura el precio "desde S/ X" por proyecto y tipología.

## 2. Referentes US y qué tomar de cada uno

| Plataforma | Modelo | Qué aplicar a InmoNExo |
|---|---|---|
| **Zonda** (adquirida por CoStar) | Plataforma de datos de vivienda nueva: tracking del ciclo completo a nivel lote/comunidad (inventario, ventas, estado), research económica, forecasts. | Tracking por proyecto con inventario y ventas = producto por el que la industria paga. Es el análogo directo. |
| **Altos Research** | Datos semanales por ZIP + Market Action Index + reportes branded; desde ~US$80/mes. | Índice propio + reportes automáticos semanales por distrito sobre PriceSnapshots. Modelo de monetización accesible. |
| **Yardi Matrix** | ~23M unidades; pipeline de construcción, absorción, forecasts; reportes nacionales gratuitos (adquisición) + detalle por suscripción. | "Cuánta oferta entra y a qué velocidad se absorbe" — LA pregunta que nadie responde en Perú a nivel proyecto. |
| **Zillow New Construction** | "Community pages" públicas por proyecto (SEO) + "Promoted Communities" con presupuesto de leads. | Páginas públicas por proyecto/desarrollador = máquina SEO gratis que alimenta el funnel B2B. |
| **Homes.com (CoStar)** | "Your listing, your lead": no revender leads; diferenciación por confianza. | Posicionamiento: proveedor neutral de inteligencia que no compite con los canales de venta de los developers. |

**Fuentes de datos públicos de Perú para enriquecer:** CAPECO PME (pme.pe — ventas trimestrales de Lima), Informe Económico de la Construcción (iec.capeco.org — IEC98: +6.8% para 2026), INEI (licencias de obra municipales).

## 3. Features recomendadas

**Ya en el roadmap (validadas por esta investigación):** 01 feed de eventos (= Altos/Yardi market updates), 02 histórico de precios (= Zillow/Zonda), 04 compare, 05 export, 08 activity score (= Altos Market Action Index), 10 auth/workspaces (= monetización B2B).

**Nuevas:**

1. **Índice InmoNExo por distrito** → ticket 11: semanal (vs mensual de Urbania), por distrito/desarrollador, metodología pública, calculado desde PriceSnapshots. Competición directa con Urbania Índex pero mejor.
2. **Tracking de inventario/absorción por tipología** → ticket 12: unidades disponibles vs vendidas por UnitType y su velocidad de absorción (estilo Zonda). La feature más diferenciadora; nadie la tiene en Perú.
3. **Páginas públicas por proyecto/desarrollador** (SEO, estilo Zillow community pages).
4. **Reporte semanal automático** (PDF/newsletter) por distrito — modelo Altos: adquisición B2B + autoridad.
5. **Enriquecimiento con CAPECO/INEI**: contrastar oferta scrapeada con cifras oficiales en reportes (credibilidad B2B).

## 4. Tesis de competencia

Urbania vende atención; InmoNExo vende certeza. Los clientes de Urbania (desarrolladores, consultoras, bancos, tasadores) necesitan lo que Urbania no produce: histórico estructurado, pipeline y absorción a nivel proyecto. Riesgo principal: que QuintoAndar profundice su data. Mitigación: foco en preventa de developers desde webs públicas + datos oficiales, y velocidad en índice e inventario.

## Fuentes

- [Urbania — LinkedIn](https://pe.linkedin.com/company/urbania-peru)
- [QuintoAndar adquiere Navent (PR Newswire)](https://www.prnewswire.com/news-releases/quintoandar-adquiere-navent-para-reforzar-su-oferta-inmobiliaria-en-latinoamerica-843076872.html)
- [Urbania — planes para profesionales](https://urbania.pe/publica-tu-aviso/profesional.html)
- [Urbania 3D](https://urbania3d.app/)
- [Roomver — comparativa de portales peruanos](https://www.roomver.com/5-portales-inmobiliarios-gratuitos-de-peru/1874/)
- [Zonda Home](https://zondahome.com/)
- [Altos Research](https://altosresearch.com/) · [Market Action Index](https://www.altosresearch.com/market_reports) · [pricing (~US$80/mes)](https://blog.iq.dwellsy.com/altos-research-data-overview-2026-housing-market-analytics-and-real-time-pricing-data/)
- [Yardi Matrix — forecast de completions](https://www.yardimatrix.com/blog/us-multifamily-completions-forecast-upward/) · [National Report (PDF)](https://irp.cdn-website.com/cd05d96c/files/uploaded/Matrix_Multifamily_National_Report-March_2025.pdf)
- [Zillow — New Construction Advertising](https://www.zillow.com/new-construction-advertising/) · [Promoted Communities T&C](https://www.zillow.com/new-construction-advertising/promoted-communities-terms/)
- [RISMedia — "your listing, your lead" (Homes.com)](https://www.rismedia.com/2023/11/03/how-the-costar-playbook-got-homes-com-to-no-2/)
- [CAPECO PME](https://www.pme.pe/) · [CAPECO IEC](https://iec.capeco.org/) · [INEI — estadísticas de construcción](https://www.inei.gob.pe/media/MenuRecursivo/publicaciones_digitales/Est/Lib1758/cap18/cap18.pdf)
