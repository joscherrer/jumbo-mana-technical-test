<script setup lang="ts">
import { Slider } from '@/components/ui/slider';

const props = defineProps<{
    name: string;
    max: number;
    min: number;
    step: number;
    description: string;
    default?: number[];
}>();

const model = defineModel()

</script>

<template>
    <div class="my-2">
        <div class="space-y-2">
            <label class="text-sm font-medium leading-none">{{ props.name }}</label>
        </div>
        <Slider class="mt-2" v-model="model" :default-value="props.default" :max="props.max" :min="props.min"
            :step="props.step" />
        <div class="flex justify-between text-muted-foreground text-sm mt-2">
            <span class="text-wrap">{{ props.description }}</span>
            <span class="mx-2 text-nowrap">{{ model?.join(' - ') }}</span>
        </div>
    </div>
</template>
