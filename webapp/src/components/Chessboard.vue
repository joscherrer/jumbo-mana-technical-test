<script setup lang="ts">
import { onMounted } from 'vue'

import Spinner from './Spinner.vue'

import 'cm-chessboard/assets/chessboard.css'
import { Chessboard } from "cm-chessboard/src/Chessboard.js";
import { FEN } from "cm-chessboard/src/model/Position.js";
import { Chess } from 'chess.js';

import Game from '../game.ts';

const version = defineModel('version');
const game = defineModel('game');

onMounted(() => {
    game?.value?.start();
});
</script>

<template>
    <div class="flex h-screen">
        <div id="board" class="w-3/6 m-auto"></div>
    </div>
</template>
