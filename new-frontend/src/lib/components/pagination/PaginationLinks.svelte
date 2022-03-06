<script lang="ts">
    import type {IpaginationObject} from "./paginate";

    export let paginationObject: IpaginationObject;
    export let paginationObjectChanged: () => void;
    // $: itemsCount = paginationObject.items.length;
    // $: itemsPerPage = paginationObject.itemsPerPage;
    // let currentPageNumber
    // $: {
    //     currentPageNumber = paginationObject.currentPageNumber;
    //     paginationObject = paginationObject
    // }
    //
    // $: pagesCount = paginationObject.numberOfPages;
    // $: console.log("paginationObject", paginationObject)

    function setPage(pageNumber: number) {
        paginationObject.currentPageNumber = pageNumber;
        paginationObjectChanged();
        console.log("paginationObject", paginationObject)
    }

    paginationObjectChanged()  // update on load
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

{#if paginationObject.countOfPages > 1}
    <div class="pagination">
        <button class="first" on:click={()=>setPage(1)}>&lt&lt</button>
        <button class="prev" on:click={()=>setPage(Math.max(paginationObject.currentPageNumber - 1, 1))}>&lt</button>
        <div>{paginationObject.currentPageNumber}/{paginationObject.countOfPages}</div>
        <button class="next" on:click={()=>setPage(Math.min(paginationObject.currentPageNumber + 1, paginationObject.countOfPages))}>&gt</button>
        <button class="last" on:click={()=>setPage(paginationObject.countOfPages)}>&gt&gt</button>
    </div>
{/if}