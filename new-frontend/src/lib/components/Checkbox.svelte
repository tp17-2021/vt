<script lang="ts">
    export let checked: boolean = false;
    export let size: number = 60 // size in pixels;
</script>

<style lang="scss">
  input {
    accent-color: var(--darkyellow);
    border: 2px black;
    pointer-events: none;  /* Disabled checkbox - is enabled only by externally setting checked variable */
  }
</style>

<input type="checkbox" bind:checked style="width: {size}px; height: {size}px" />