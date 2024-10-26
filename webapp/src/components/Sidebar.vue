<script setup lang="ts">
import { ref, onMounted } from 'vue';
import {
    Select,
    SelectContent,
    SelectGroup,
    SelectItem,
    SelectLabel,
    SelectTrigger,
    SelectValue,
} from '@/components/ui/select';
import {
    FormControl,
    FormDescription,
    FormField,
    FormItem,
    FormLabel,
    FormMessage,
} from '@/components/ui/form'
import { Slider } from '@/components/ui/slider';
import { Button } from '@/components/ui/button';
import { Separator } from '@/components/ui/separator';
import { cn } from '@/lib/utils';

import { Checkbox } from '@/components/ui/checkbox';

import ColorModeToggle from './ColorModeToggle.vue';
import SliderControl from './SliderControl.vue';
import Game from '../game.ts';

const version = defineModel('version');
const game: Game = defineModel('game');
const emit = defineEmits<{
    newGame: [max_depth: number, plies: number[], max_cp: number, max_pv: number]
}>();

const max_depth = ref([10]);
const plies = ref([16, 26]);
const max_cp = ref([5]);
const max_pv = ref([5]);

function newGame() {
    emit('newGame', {
        max_depth: max_depth.value[0],
        min_ply: plies.value[0],
        max_ply: plies.value[1],
        max_cp: max_cp.value[0],
        max_pv: max_pv.value[0]
    });
}

onMounted(() => {
    version.value = 'v1';
});

function onSubmit(e: Event) {
    console.log('Submit', e);
}

</script>

<template>
    <div class="min-w-40 max-w-60 px-2 my-2">
        <div class="flex mb-4 space-x-2">
            <Button variant="outline" class="flex-auto mb-2" @click="newGame">New game</Button>
            <ColorModeToggle class="flex-initial" />
        </div>
        <div id="params" class="flex-initial">
            <h1 class="text-lg">Game settings</h1>
            <Separator class="mt-1 mb-2" />
            <SliderControl name="Depth" :max="30" :min="1" :step="1" description="Max depth used during eval"
                v-model="max_depth" />

            <SliderControl name="Ply range" :max="30" :min="1" :step="1" description="Min and max number of plies"
                v-model="plies" />
            <SliderControl name="Max cp" :max="10" :min="1" :step="1" description="Maximum Centipawn advantage allowed"
                v-model="max_cp" />
            <SliderControl name="Max pv" :max="10" :min="1" :step="1" description="Maximum number of PVs to compute"
                v-model="max_pv" />
        </div>
        <div v-if="game" id="stats" class="flex-initial mt-9">
            <h1 class="text-lg">Game information</h1>
            <Separator class="mt-1 mb-2" />
            <div class="grid grid-cols-3 gap-2">
                <div class="font-bold">Turn</div>
                <div class="col-span-2">{{ game.boardInfo.turn }}</div>
                <div class="font-bold">Score</div>
                <div class="col-span-2">{{ game.boardInfo.score > 0 ? "+" : "" }}{{ game.boardInfo.score }} cp</div>
                <div class="font-bold">Ply</div>
                <div class="col-span-2">{{ game.boardInfo.ply }}</div>
            </div>
        </div>

    </div>
</template>

<style></style>
