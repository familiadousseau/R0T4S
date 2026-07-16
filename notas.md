# R0T4S — Notas do projeto (para continuar noutro ambiente)

> **Como usar este ficheiro:** no Claude Code, diz *"lê o NOTAS.md e o index.html para perceberes o projeto"*.
> O `index.html` está todo comentado em português e é a fonte de verdade. Este ficheiro é o mapa.

**Versão atual:** v15.04-fluxo (o número está no rodapé da app — serve para saber se a publicação no GitHub Pages pegou; se o rodapé mostrar versão antiga, é cache da PWA: reinstalar o atalho).

---

## 1. O que é a app

Web-app **de ficheiro único** (`index.html`, ~170 KB, tudo inline: HTML+CSS+JS) para o **Renan**, entregador CTT/PAC na zona de **Viana do Castelo**. Publicada em **GitHub Pages** (HTTPS obrigatório). Instalável como **PWA** (`manifest.json` + `sw.js`).

Acompanham o `index.html`:
- `sw.js` — service worker (cache atual: `r0t4s-v5`). **Pré-carrega o Leaflet** na instalação.
- `manifest.json` — nome curto "Rotas", verde #1B5E20, standalone.
- `icon-192.png`, `icon-512.png`, `icon-180.png`, `favicon-32.png`.

**Regra de ouro:** foco no **destinatário**. Vários pacotes na mesma morada = **UMA paragem**.

---

## 2. Fluxo de trabalho real (o dia do Renan)

1. **À noite — pré-atribuição** (🌙): aponta a câmara ao ecrã do PDA (Samsung bloqueado por MDM, não dá para exportar de lá). Lê **código + morada** e guarda numa pré-lista (localStorage `preAtrib`).
2. **De manhã — captura/bip**: no galpão, bipa o código de barras de cada pacote. Se o código está na pré-lista → entra **na hora**, sem OCR, só mostrando o número a marcar no pacote.
3. Marca o nº no pacote → arruma no carro pela ordem inversa da rota (mapa de carga).
4. **Otimizar** → mapa + rota.
5. **Exportar**: CSV (Spoke, Android) ou PDF (iPhone).

### Dois formatos de entrada
- **Texto/colar** = empresa **PAC**.
- **Imagem/foto do ecrã** = empresa **CTT**.
- Nome dos ficheiros: `entrega_dia_X_mes_Y`, com sufixos `.2`, `.3` para lotes no mesmo dia (o 1º não tem sufixo).

---

## 3. Regras que NÃO são óbvias no código (não partir)

- **O leitor de código de barras/QR é PRIORIDADE ABSOLUTA.** Nasce no arranque da app (não à espera do botão), insiste até estar pronto, lê **direto do vídeo** (~40 leituras/s, sem copiar frames). O OCR **nunca** ocupa o lugar do código. Barras primeiro; só se não houver barras em ~4-6s é que o OCR lê o código escrito.
- **Guarda os DOIS códigos** (barras E QR do mesmo pacote) — busca por qualquer um.
- **Código do objeto CTT = formato S10**: `2 letras + 9 dígitos + 2 letras` (ex.: `DW481062437PT`). No ecrã do PDA há iscos (código postal, telefone, referência, data, e o pacote da lista de fundo). Desempate: o código certo **aparece 2×** (título + "Objetos do serviço") e está **mais acima**. Regex `RE_S10`. Ignora telefones (9 díg. começados por 9/2) e a linha do CP.
- **OCR da morada é ancorado** no "Destinatário" — lê só rua→código postal, rápido, não mapeia a etiqueta toda.
- **CSV Spoke = exatamente 4 colunas**: `"Address Line 1"`, `"City"`, `"Zip/Postal Code"`, `"ID"`. Divide no código postal português (NNNN-NNN): antes → Address Line 1; depois (localidade) → City. **Preserva a ordem original das paragens** (nunca renumera). Duplicados ganham asterisco. Cidade por omissão: **Viana do Castelo** (nunca Braga).
- **PDF**: 2 colunas (Nº / Endereço), ruas agrupadas, linhas alternadas branco/verde-claro, cabeçalho verde-escuro; mais mapa de carga (ordem DECRESCENTE: 1º a entrar = última paragem) e índice por pacote.
- **Comparação de códigos é normalizada** (`normCod`): ignora maiúsculas, espaços, hífenes, pontos. Isto evita links falhados entre pré-lista e bip.

---

## 4. Como funcionam as peças grandes

- **Geocodificação em segundo plano** (fila `geoFila`): cada morada entra na fila mal é registada (pré-atribuição, bip, captura, voz, escrita, importação). ~1 pesquisa/segundo. **Memória persistente** em `localStorage` (`geoCache`, cap 600) — morada já localizada não volta à internet. Chip de progresso na aba Otimizar.
- **Pipeline PT** (`geocodeExplicado`): **encontrar sempre > validar com perfeição**. Dois motores gratuitos em cascata: **Nominatim** + **Photon** (Komoot). Cinco redes de segurança antes de dar erro (morada+CP → rua+freguesia/concelho → centro do CP via GeoAPI.pt → melhor tentativa "a confirmar" → zona do CP). `RAIO_MAX_KM=12`. Sem CP português → pesquisa internacional (a app funciona fora de Portugal). CP igual é aceite sempre.
- **Só código postal** escrito (ex. `4925-184`) → devolve as **ruas desse CP** (`ruasDoCP`, base GeoAPI.pt).
- **Localização do utilizador** obtida em fundo no arranque e renovada de 5 em 5 min; as sugestões de morada são ordenadas **por proximidade** (as entregas são perto).
- **Mapa interativo** (Leaflet, embutido na aba Otimizar): a caixa está **sempre presente**. Pinos arrastáveis (verde=ok, amarelo="a confirmar"/aproximado, azul=base). Arrastar grava as coordenadas à mão (`via='corrigido no mapa'`, não volta a ser geocodificada). Fundo dos azulejos com recurso: OSM → CARTO se falhar. Reordenar paragens e editar morada (✏️) **no mesmo bloco da rota** (fundido — não há caixas separadas). Arrastar pelo punho ⠿ (rato + toque).
- **Modo escuro** (v15.01): segue o sistema + interruptor 🌙/☀️ no topo (persistente). Cores via variáveis CSS (`--cartao`, `--papel`, `--tinta`, etc.) + bloco `@media (prefers-color-scheme: dark)` e `:root[data-tema]`.
- **Persistência**: `trabalhoDia` (auto, debounce), `preAtrib`, `geoCache`. Retoma com dupla confirmação. **Cuidado:** o `JSON.stringify` do trabalho ignora a chave `grupo` (evita referência circular que já partiu a gravação uma vez — ver histórico).

---

## 5. Ligação manual pré↔bip (v15.04 — importante)

Se o código guardado na pré-lista **for diferente** do impresso nas barras físicas (acontece quando o ecrã do PDA não tinha barras e o OCR guardou os dígitos escritos), o bip não bate. Rede de segurança: no cartão de captura aparece **"🌙 É um pré-atribuído? Ligar sem recapturar"** → escolhes o pré → entra com a morada do pré e **guarda os dois códigos juntos** (aprende: o rebip seguinte já dá amarelo).

---

## 6. Pontos sensíveis / o que costuma partir

- **Regressões recorrentes** no fluxo de captura (o link pré→bip, a câmara que fica aberta, o mapa branco). Correr a **bateria de testes** (secção 8) ANTES de cada entrega.
- **Mapa branco**: quase sempre é o **CSS do Leaflet** que não carregou (JS carrega, CSS não → quadrado branco). O sw v5 pré-carrega ambos; a app deteta e recarrega o CSS antes de criar o mapa. Se voltar: reinstalar o atalho da PWA (força sw novo).
- **Cache da PWA**: qualquer "não atualizou" resolve-se confirmando a versão no rodapé e, se preciso, reinstalando o atalho. Cada entrega sobe o nº de versão (rodapé) e o `CACHE` do sw.
- **Câmara**: só ligada dentro do fluxo (captura ou pré aberta). `pararCam()` corta a stream de verdade (bateria/indicador do Android). Captura e pré-atribuição fecham o painel um do outro **sem apagar dados**.
- **Edições em silêncio**: ao editar o `index.html` por script, SEMPRE validar com `assert` e verificar sintaxe de cada `<script>` — várias edições já falharam caladas ou deixaram chaves órfãs `}`.

---

## 7. O que ficou por fazer / ideias

- **Login + conta mestre + proteção contra cópia**: decidido **adiar**. Conclusão técnica: impedir cópia numa web-app é impossível sem **servidor** (o `index.html` está no telemóvel do utilizador). Se um dia for para **vender** a outros entregadores, o caminho é um servidor gratuito (Supabase/Firebase) a guardar contas e a verificar quem pagou — o ecrã de login liga-se a ele depois, sem deitar fora o trabalho. "Sem pagar" é possível; "sem servidor" não.
- Afinação fina de tempos (ex.: vantagem das barras sobre o OCR nos ecrãs).
- Export próprio para reimportação perfeita com códigos.

---

## 8. Bateria de testes (correr antes de cada alteração)

Ambiente: sandbox sem internet → usar **Playwright com stubs** (câmara, OCR, BarcodeDetector, Leaflet, SpeechRecognition, rotas de rede). Cenários mínimos que **têm de passar**:

1. **Bipar pré-atribuído** → confirmação instantânea (~ms), ecrã do número com badge PRÉ, entra na Lista com a morada do pré, herda coordenadas, sai da pré-lista, **sem pedir OCR**.
2. **Rebip do mesmo código** → ecrã amarelo "já atribuído" com o nº.
3. **Código novo** → captura normal com OCR (cartão com código + morada).
4. **Códigos diferentes pré vs barras** → cartão abre com botão "🌙 Ligar", 2 toques ligam, guarda os dois códigos, aprende.
5. **Normalização**: pré `dw 481-062-437 pt` vs bip `DW481062437PT` → liga.
6. **Persistência**: gravar sobrevive à otimização (JSON válido, sem circular).
7. **Reordenar** paragens → exportação (CSV/PDF) segue a nova ordem.
8. **Agrupar**: mesma morada = 1 paragem; mesma rua nº diferente = paragens separadas.
9. **Geocodificação**: com GeoAPI a falhar (429), moradas ainda localizadas (redes de segurança); repetir morada vem da cache.
10. **Só CP** (`4925-184`) → devolve ruas.
11. **Mapa**: caixa sempre presente; Leaflet bloqueado → mensagem, não branco; OSM falha → troca CARTO.
12. Sintaxe: `new Function()` sobre cada `<script>` do `index.html`.

Verificar sempre: nenhuma função `onclick` sem definição; nenhum id duplicado; nº de versão atualizado no rodapé + `CACHE` do sw.

---

## 9. Histórico de versões recentes

- **v15.04-fluxo** — normalização de códigos; ligação manual pré↔bip que aprende; auditoria do fluxo crítico.
- **v15.03-rota** — sugestões por CP; localização em fundo + proximidade; três blocos (rota/ordem/edição) fundidos num; arrasto sem seleção de texto; frase óbvia do mapa removida.
- **v15.02-mapa** — Leaflet pré-carregado no sw; azulejos com servidor alternativo; vigia do mapa branco.
- **v15.01-escuro** — modo escuro (sistema + interruptor).
- **~v14** — geocodificação em fundo + cache; mapa interativo (arrastar/reordenar/"a confirmar"); pipeline com Photon; muitas correções de câmara e pré-atribuição.
