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

    // ---- Cenário 5: código-lixo acumulado ANTES não pode bloquear o match do código certo a seguir
    // (bug real relatado: código lido corretamente mas não confirmou na hora porque uma leitura
    // espúria anterior já tinha entrado em capCodigos)
    await page.evaluate(() => {
      preAtribuidos.length = 0; pacotes.length = 0; capCodigos.length = 0;
      preAtribuidos.push({ cod: 'DW481062437PT', cod2: '', morada: 'Rua Escura nº 5, 4900-222 Viana do Castelo' });
      capCodigos.push({ val: 'LIXO1234', tipo: 'code_128' });   // leitura espúria já acumulada
    });
    let r5 = await page.evaluate(() => {
      const decisao = decidirDeteccoes([{ rawValue: 'DW481062437PT', format: 'code_128' }]);
      return decisao.tipo;
    });
    ok('código certo é reconhecido mesmo com código-lixo já acumulado em capCodigos', r5 === 'pre');

    // ---- Cenário 6: tolerância a confusões típicas de OCR (0/O, 1/I/L, 5/S, 8/B) ----
    await page.evaluate(() => {
      preAtribuidos.length = 0; pacotes.length = 0;
      preAtribuidos.push({ cod: 'DW4B1O62437PT', cod2: '', morada: 'Rua Torta nº 7, 4900-333 Viana do Castelo' });
    });
    let r6 = await page.evaluate(() => !!encontrarPre('DW481062437PT'));
    ok('encontrarPre tolera confusão OCR B/8 e O/0 num único caráter', r6 === true);

    // ---- Cenário 7: canonicalização da morada a partir do resultado do geocoder ----
    let r7 = await page.evaluate(() => {
      const comRua = formatarMoradaOficial({ address: { road:'Rua das Flores', house_number:'12', postcode:'4900-000', city:'Viana do Castelo' } });
      const semRua = formatarMoradaOficial({ address: { postcode:'4900-000', city:'Viana do Castelo' } });
      return { comRua, semRua };
    });
    ok('formatarMoradaOficial monta rua + nº + CP + localidade', r7.comRua === 'Rua das Flores nº 12, 4900-000 Viana do Castelo');
    ok('formatarMoradaOficial devolve null sem nome de rua (não canonicaliza às cegas)', r7.semRua === null);

    // ---- Cenário 9: ordenarPorRua agrupa mesma morada e mesma rua lado a lado,
    // sem mexer nos índices originais (apenas a ordem de apresentação) ----
    let r9 = await page.evaluate(() => {
      const lista = [
        { morada:'Rua A nº 1, 4900-000 Viana do Castelo' },   // i=0
        { morada:'Rua B nº 5, 4900-000 Viana do Castelo' },   // i=1
        { morada:'Rua A nº 3, 4900-000 Viana do Castelo' },   // i=2
        { morada:'Rua A nº 1, 4900-000 Viana do Castelo' },   // i=3 — mesma morada que i=0
        { morada:'' },                                          // i=4 — sem morada
      ];
      const vista = ordenarPorRua(lista);
      return vista.map(v => v.i);
    });
    ok('ordenarPorRua agrupa mesma rua/morada lado a lado e deixa "sem morada" no fim', JSON.stringify(r9) === JSON.stringify([0,3,2,1,4]));

    // ---- Cenário 10: botão HERE WeGo gera o link certo (com e sem coordenadas) ----
    let r10 = await page.evaluate(() => {
      pacotes.length = 0;
      pacotes.push({ nPacote:1, morada:'Rua Sol nº 2, 4900-050 Viana do Castelo', lat:41.69, lon:-8.83 });
      pacotes.push({ nPacote:2, morada:'Rua Sombra nº 4, 4900-060 Viana do Castelo', lat:null, lon:null });
      const abertos = [];
      const originalOpen = window.open;
      window.open = (u) => abertos.push(u);
      abrirMapa(0, 'here');
      abrirMapa(1, 'here');
      window.open = originalOpen;
      return abertos;
    });
    ok('HERE WeGo com coordenadas usa lat,lon', r10[0] === 'https://wego.here.com/directions/drive//41.69,-8.83');
    ok('HERE WeGo sem coordenadas cai para a morada em texto', r10[1].startsWith('https://wego.here.com/directions/drive//') && decodeURIComponent(r10[1].split('drive//')[1]).includes('Rua Sombra'));

    // ---- Cenário 11: sintaxe de validação já corre à parte (npm run validar) ----

  } finally {
    await browser.close();
    await new Promise(res => servidor.close(res));
  }

  console.log(`\n${passados} passaram, ${falhas} falharam.`);
  process.exit(falhas ? 1 : 0);
}

main().catch(e => { console.error(e); process.exit(1); });
