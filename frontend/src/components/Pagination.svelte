<script lang="ts">
    export let itemsCount
    export let itemsPerPage
    export let currentPage

    $: pagesCount = Math.ceil(itemsCount / itemsPerPage)
    $: console.log(itemsCount, itemsPerPage, pagesCount)
</script>

<style lang="scss">
  .pagination {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 10px;
    font-size: 1.5rem;

    button {
      background-color: var(--lightgray);
      border: none;
      color: green;
      width: 60px;
      height: 60px;
      font-weight: bold;
    }
  }
</style>

{#if pagesCount > 1}
    <div class="pagination">
        <button class="first" on:click={()=>currentPage=1}>&lt&lt</button>
        <button class="prev" on:click={()=>currentPage=Math.max(currentPage - 1, 1)}>&lt</button>
        <div>{currentPage}/{pagesCount}</div>
        <button class="next" on:click={()=>currentPage=Math.min(currentPage + 1, pagesCount)}>&gt</button>
        <button class="last" on:click={()=>currentPage=pagesCount}>&gt&gt</button>
    </div>
{/if}