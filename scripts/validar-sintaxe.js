#!/usr/bin/env node
// Valida a sintaxe de cada <script> inline do index.html antes de publicar.
// Não executa a app — só confirma que o JavaScript está bem formado, para
// apanhar chavetas órfãs ou erros de edição antes de irem para produção.
'use strict';
const fs = require('fs');
const path = require('path');
const vm = require('vm');

const ficheiro = path.join(__dirname, '..', 'index.html');
const html = fs.readFileSync(ficheiro, 'utf8');

const regex = /<script(\s[^>]*)?>([\s\S]*?)<\/script>/gi;
let match, indice = 0, erros = 0, validados = 0;

while ((match = regex.exec(html)) !== null) {
  const atributos = match[1] || '';
  const corpo = match[2];
  indice++;
  if (/\bsrc\s*=/.test(atributos)) continue;        // scripts externos (CDN): nada a validar aqui
  if (!corpo.trim()) continue;                        // bloco vazio

  try {
    new vm.Script(corpo, { filename: `index.html <script #${indice}>` });
    validados++;
  } catch (e) {
    erros++;
    console.error(`✗ Erro de sintaxe no <script> nº ${indice}: ${e.message}`);
  }
}

if (erros > 0) {
  console.error(`\n${erros} bloco(s) com erro de sintaxe. Corrige antes de publicar.`);
  process.exit(1);
}
console.log(`✓ Sintaxe válida — ${validados} bloco(s) de <script> verificados.`);
