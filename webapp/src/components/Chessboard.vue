<script setup lang="ts">
import { onMounted } from 'vue'

import Spinner from './Spinner.vue'

import 'cm-chessboard/assets/chessboard.css'
import { Chessboard } from "cm-chessboard/src/Chessboard.js";
import { FEN } from "cm-chessboard/src/model/Position.js";
import { Chess } from 'chess.js';

import Game from '../game.ts';

import axios, { isCancel, AxiosError } from 'axios';
const client = axios.create({
    baseURL: 'http://localhost:8000',
    timeout: 1000,
    headers: {
        'Content-Type': 'application/json',
    },
});

const version = defineModel('version');
const game = defineModel('game');

onMounted(() => {
    game?.value?.start();
});
</script>

<template>
    <div id="board" class="m-2"></div>
</template>
