<script lang="ts">
    export let checked: boolean = false;
    export let size: number = 60 // size in pixels;
</script>

<style lang="scss">
  input {
    accent-color: var(--darkyellow);
    border: 2px black;
  }
</style>

<input type="checkbox" bind:checked style="width: {size}px; height: {size}px" />