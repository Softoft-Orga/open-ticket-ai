<script lang="ts" setup>
import YamlTree from './YamlTree.vue'
import tagYaml from '../../data/tags.yml?raw'
</script>

<template>
    <YamlTree :source="tagYaml"/>
</template>
