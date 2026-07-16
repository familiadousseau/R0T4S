#!/usr/bin/env node
// Bateria mínima automatizada dos cenários mais frágeis descritos no notas.md (secção 8):
// ligação pré-atribuição ↔ bip, normalização de código, rebip, e agrupamento por morada.
// Não simula câmara/OCR/leitor de códigos (isso exigiria stubs pesados) — em vez disso,
// chama diretamente as funções de negócio que essas entradas de hardware acionam, que são
// precisamente as partes que o notas.md assinala como as que mais partem.
'use strict';
const { chromium } = require('playwright');
const { createServer } = require('http-server');
const path = require('path');

const PORTA = 8991;
const CHROMIUM_PATH = '/opt/pw-browsers/chromium';

let falhas = 0, passados = 0;
function ok(desc, cond){
  if(cond){ passados++; console.log(`✓ ${desc}`); }
  else{ falhas++; console.error(`✗ ${desc}`); }
}

async function main(){
  const servidor = createServer({ root: path.join(__dirname, '..') });
  await new Promise(res => servidor.listen(PORTA, res));

  const browser = await chromium.launch({ executablePath: CHROMIUM_PATH });
  const context = await browser.newContext();
  const page = await context.newPage();
  page.on('pageerror', e => console.error('  [erro na página]', e.message));

  try{
    await page.goto(`http://localhost:${PORTA}/index.html`, { waitUntil: 'load' });
    await page.waitForFunction(() => typeof window.encontrarPre === 'function');

    // ---- Cenário 1: bipar pré-atribuído → confirmação instantânea, sem OCR ----
    await page.evaluate(() => {
      preAtribuidos.length = 0; pacotes.length = 0;
      preAtribuidos.push({ cod: 'DW481062437PT', cod2: '', morada: 'Rua das Flores nº 12, 4900-000 Viana do Castelo' });
    });
    let r1 = await page.evaluate(() => {
      const pre = encontrarPre('DW481062437PT');
      if(!pre) return { achou:false };
      confirmarPre(pre, 'DW481062437PT');
      return {
        achou:true,
        preRestantes: preAtribuidos.length,
        pacotesCriados: pacotes.length,
        morada: pacotes[0] && pacotes[0].morada,
        pre: document.getElementById('mfPre').style.display,
      };
    });
    ok('pré-atribuído é encontrado pelo código exato', r1.achou);
    ok('confirmarPre remove da pré-lista', r1.preRestantes === 0);
    ok('confirmarPre cria 1 pacote com a morada do pré', r1.pacotesCriados === 1 && r1.morada === 'Rua das Flores nº 12, 4900-000 Viana do Castelo');
    ok('ecrã de marcação mostra o badge "pré-atribuído"', r1.pre === 'block');

    // ---- Cenário 2: normalização — código com espaços/hífenes/minúsculas ainda liga ----
    await page.evaluate(() => {
      preAtribuidos.length = 0; pacotes.length = 0;
      preAtribuidos.push({ cod: 'DW481062437PT', cod2: '', morada: 'Rua Nova nº 3, 4900-111 Viana do Castelo' });
    });
    let r2 = await page.evaluate(() => {
      const pre = encontrarPre('dw 481-062-437 pt');
      return !!pre;
    });
    ok('código com espaços/hífenes/minúsculas ainda liga ao pré (normCod)', r2 === true);

    // ---- Cenário 3: rebip do mesmo código → "já atribuído", não duplica pacote ----
    await page.evaluate(() => {
      preAtribuidos.length = 0; pacotes.length = 0;
      pacotes.push({ nPacote:1, codes:['DW481062437PT'], code:'DW481062437PT',
        morada:'Rua Nova nº 3, 4900-111 Viana do Castelo', lat:null, lon:null, ordem:null });
    });
    let r3 = await page.evaluate(() => {
      const dono = pacoteComCodigo('dw481062437pt');   // minúsculas: tem de normalizar também aqui
      return { encontrado: !!dono, nPacote: dono && dono.nPacote };
    });
    ok('pacoteComCodigo encontra o dono independente de maiúsculas/minúsculas', r3.encontrado && r3.nPacote === 1);

    // ---- Cenário 4: agrupamento — mesma morada (variações de acentos/espaços) = mesma paragem ----
    let r4 = await page.evaluate(() => {
      const a = chaveMorada('Rua das Flores, nº 12, 4900-000 Viana do Castelo');
      const b = chaveMorada('rua  das flôres nº12 4900-000 viana do castelo');
      const c = chaveMorada('Rua das Flores, nº 14, 4900-000 Viana do Castelo');
      return { iguais: a === b, diferente: a !== c };
    });
    ok('chaveMorada agrupa a mesma morada apesar de acentos/espaços diferentes', r4.iguais);
    ok('chaveMorada distingue números de porta diferentes', r4.diferente);

    // ---- Cenário 5: sintaxe de validação já corre à parte (npm run validar) ----

  } finally {
    await browser.close();
    await new Promise(res => servidor.close(res));
  }

  console.log(`\n${passados} passaram, ${falhas} falharam.`);
  process.exit(falhas ? 1 : 0);
}

main().catch(e => { console.error(e); process.exit(1); });
