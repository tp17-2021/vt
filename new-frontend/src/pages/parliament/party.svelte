<script lang="ts">
    import PartyBox from "../../lib/components/PartyBox.svelte";
    import Button from "../../lib/components/buttons/Button.svelte";
    import {parties, vote} from "../../api/stores";
    import {goto, url} from "@roxi/routify";
    import {get} from "svelte/store";
    import type {IpaginationObject} from "../../lib/components/pagination/paginate";
    import {searchAndPaginate} from "../../lib/components/pagination/paginate";
    import PaginationLinks from "../../lib/components/pagination/PaginationLinks.svelte";
    import Warning from "../../lib/components/Warning.svelte";
    import Modal from "../../lib/components/Modal.svelte";
    import VirtualInput from "../../lib/components/VirtualInput.svelte";

    function chooseParty(party) {
        if (party == null) {
            $vote.party_id = null;
        }
        else {
            $vote.party_id = party._id;
        }
        $vote.candidate_ids = [];
    }

    function next() {
        if ($vote.party_id == null) {
            $goto("/parliament/confirm/");
        }
        else    {
            $goto("/parliament/candidates/");
        }
    }

    // // --- pagination and search ---
    let paginationObject: IpaginationObject = {
        items: get(parties),
        paginatedItems: [],
        searchTerm: "",
        currentPageNumber: 1,
        countOfPages: 1,
        itemsPerPage: 5,
        searchBy: ["name"],
    }

    function paginateParties() {
        searchAndPaginate(paginationObject)  // paginationObject is updated inside this function
        paginatedParties = paginationObject.paginatedItems
    }

    let paginatedParties = []
    $: console.log("$vote.party_id", $vote.party_id);


    // modals
    let openModal
    let searchValue = ""

    function searchValueChanged(searchValue) {
        console.log("searching", searchValue);
        paginationObject.currentPageNumber = 1
        paginationObject.searchTerm = searchValue
        paginateParties()
    }

    $: searchValueChanged(searchValue);
</script>

<style>
    #search {
        margin-bottom: 1rem;
    }
    .parties {
        height: calc(100vh - 450px);
        overflow: auto;
        margin-bottom: 1rem;
    }
</style>

<h2>Kandidujúce strany:</h2>
<VirtualInput bind:value={searchValue} type="text" id="search" placeholder="Vyhľadajte kandidujúcu stranu"/>
<!--<input type="text" id="search" placeholder="Vyhľadajte kandidujúcu stranu" on:input={e => {-->
<!--    paginationObject.currentPageNumber = 1-->
<!--    paginationObject.searchTerm = e.target.value-->
<!--    paginateParties(paginationObject)-->
<!--}}>-->

<p><i>Kliknutím označte stranu, ktorú chcete voliť.</i></p>
<div class="parties">
    {#if paginatedParties.length === 0}
        <Warning text="Neboli nájdené žiadne kandidujúce strany vyhovujúce vášmu vyhľadávaniu" />
    {/if}
    {#each paginatedParties as party}
        <div on:click={() => chooseParty(party._id === $vote.party_id ? null : party)}>
            <PartyBox
                    {party}
                    isSelected={party._id === $vote.party_id}
                    showCheckbox={true}
            />
        </div>
    {/each}
</div>
<PaginationLinks paginationObject={paginationObject} paginationObjectChanged={paginateParties}/>
<Button on:click={openModal} type="primary">Potvrdiť</Button>

{#if $vote.party_id !== null}
    <Modal bind:openModal yesCallback={()=>next()} yesTxt="Potvrdiť" cancelTxt="Upraviť">
        <span slot="title">Zvolili ste</span>
        <PartyBox party={$parties.find(party => party._id === $vote.party_id)} />
    </Modal>
{:else}
    <Modal bind:openModal yesCallback={()=>next()} yesTxt="Odoslať prázdny hlas" cancelTxt="Upraviť">
        <span slot="title">Nezvolili ste žiadnu stranu</span>
        <span slot="subtitle">Naozaj chcete odoslať prázdny hlas?</span>
    </Modal>
{/if}