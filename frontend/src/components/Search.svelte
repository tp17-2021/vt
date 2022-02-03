<script>
    export let title;
    export let filter;
    export let placeholder;
</script>

<style lang="scss">
  .search {
    display: flex;
    justify-content: space-between;

    button {
      background-color: var(--blue);
      border: none;
      color: white;
    }
  }
</style>

<div class="search">
    <h2>{title}</h2>
    <div>
        <input type="text" bind:value={filter} placeholder={placeholder}>
        <button><i class="fas fa-search"></i></button>
    </div>
</div>