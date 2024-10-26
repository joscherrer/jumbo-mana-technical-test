<script setup lang="ts">
import { ref } from 'vue';
import Game from './game.ts';
import Chessboard from './components/Chessboard.vue';
import Sidebar from './components/Sidebar.vue';
import { FEN } from "cm-chessboard/src/model/Position.js";

import Spinner from './components/Spinner.vue';

import axios, { isCancel, AxiosError } from 'axios';

const api_url = import.meta.env.VITE_API_URL;

const client = axios.create({
    baseURL: api_url,
    timeout: 1000,
    headers: {
        'Content-Type': 'application/json',
    },
});

const version = defineModel('version');
const game = defineModel('game');
const landed = ref(true);
const waitingForGame = ref(false);

function onNewGame(settings?: any) {
    console.log('New game', settings);
    landed.value = false;
    waitingForGame.value = true;
    client.get(`${version.value}/game/new`, { timeout: 60000, params: settings })
        .then((response) => {
            game.value = new Game("board", response.data);
        })
        .catch((error: AxiosError) => {
            if (isCancel(error)) {
                console.log('Request canceled', error.message);
                return;
            }
            console.log('Error', error.message);
            console.log('Detail', error.response?.data.detail || '');
            console.log('Starting with default position');
            game.value = new Game("board", {
                fen: FEN.start,
                turn: 'white',
                score: 0,
            });
        })
        .finally(() => {
            console.log('Game started');
            waitingForGame.value = false;
        });
}

</script>

<template>
    <div class="pr-2 h-screen">
        <div class="flex space-x-2">
            <div class="flex-auto">
                <div v-if="landed">
                    <div class="flex h-80">
                        <div class="m-auto">
                            <p class="text-3xl">To start, press the "New game" button 🡥</p>
                        </div>
                    </div>
                </div>
                <Chessboard v-if="!waitingForGame" v-model:version="version" v-model:game="game" />
                <div v-else>
                    <div class="flex h-screen">
                        <div class="m-auto">
                            <Spinner class="text-center" />
                            <div>
                                <p class="text-3xl">Generating a fair game</p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            <Sidebar @newGame="onNewGame" class="flex-none" v-model:version="version" v-model:game="game" />
        </div>
    </div>
</template>

<style scoped>
.logo {
    height: 6em;
    padding: 1.5em;
    will-change: filter;
    transition: filter 300ms;
}

.logo:hover {
    filter: drop-shadow(0 0 2em #646cffaa);
}

.logo.vue:hover {
    filter: drop-shadow(0 0 2em #42b883aa);
}
</style>
