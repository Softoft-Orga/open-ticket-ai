<script lang='ts' setup>
import YamlTree from './YamlTree.vue'
import tagYaml from './tags.yml?raw'
</script>

<template>
    <div class="rounded-xl border border-slate-800 bg-slate-900/70 p-4 shadow-xl shadow-black/40">
        <YamlTree :source="tagYaml"/>
    </div>
</template>
