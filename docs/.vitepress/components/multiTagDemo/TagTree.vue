<script lang="ts" setup>
import YamlTree from './YamlTree.vue'
import tagYaml from './tags.yml?raw'
</script>

<template>
    <YamlTree :source="tagYaml"/>
</template>
