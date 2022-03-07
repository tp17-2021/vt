<script lang="ts">
    import {Icandidate, vote} from "../../api/stores";
    import CandidateBox from "../../lib/components/CandidateBox.svelte";
    import Button from "../../lib/components/buttons/Button.svelte";
    import {goto} from "@roxi/routify";
    import {IpaginationObject, searchAndPaginate} from "../../lib/components/pagination/paginate";
    import PaginationLinks from "../../lib/components/pagination/PaginationLinks.svelte";
    import {findCandidateById, findCandidatesByPartyId} from "../../lib/helpers";
    import BackButton from "../../lib/components/buttons/BackButton.svelte";
    import Modal from "../../lib/components/Modal.svelte";
    import Warning from "../../lib/components/Warning.svelte";



    /**
     * If candidateId is in $vote.candidate_ids, remove him
     * else add him if there are less than maxCandidates candidates
     *
     * @param candidateId - candidate id to add or remove
     */
    function switchCandidate(candidateId: number) {
        if ($vote.candidate_ids.includes(candidateId)) {
            $vote.candidate_ids = [...$vote.candidate_ids.filter(id => id !== candidateId)]
        } else {
            if ($vote.candidate_ids.length < maxCandidates) {
                $vote.candidate_ids = [...$vote.candidate_ids, candidateId]
            }
            else {
                openErrorModal()
            }
        }
        console.log("$vote.candidate_ids", $vote.candidate_ids)
    }

    function next() {
        $goto("/parliament/confirm")
    }

    let maxCandidates = 5;  // max candidates to be chosen
    let candidates: Icandidate[] = []
    candidates = findCandidatesByPartyId($vote.party_id)
    console.log("available candidates", candidates)



    // --- pagination and search ---
    let paginationObject: IpaginationObject = {
        items: candidates,
        paginatedItems: [],
        searchTerm: "",
        currentPageNumber: 1,
        countOfPages: 1,
        itemsPerPage: 10,
        searchBy: ["first_name", "last_name", "order", "age", "occupation", "residence"],
    }
    let paginatedCandidates = []

    function paginateCandidates() {
        searchAndPaginate(paginationObject)  // paginationObject is updated inside this function
        paginatedCandidates = paginationObject.paginatedItems
    }


    // --- modal ---
    let openErrorModal;
</script>

<style lang="scss">
  #search {
    margin-bottom: 1rem;
  }

  .buttonArea {
    display: flex;
    justify-content: end;
    width: 100%;
  }

  .chosenCandidates {
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    width: 100%;
    min-height: 50px;


    .chosenCandidate {
      display: flex;
      padding: 0 2rem 0 0;
      gap: 5px;
      font-weight: bold;

      .name {
        color: #003078;
      }

      .xButton {
        color: #E54957;
        border: none;
        background: none;

        font-size: 2rem;
        margin-top: -15px;
      }
    }
  }

  .candidateCount {
    font-weight: bold;
    color: green;
  }

  .candidates {
    display: grid;
    margin-bottom: 1rem;
    height: calc(100vh - 580px);
    overflow: auto;


    .legend {
      display: grid;
      grid-template-columns: 20fr 5fr 7fr 10fr 7fr;
      gap: 10px;
      font-weight: bold;
      padding: 0 2rem;
    }
  }


  .modalCandidates {
    font-weight: bold;
    margin-bottom: 1rem;
  }
</style>

<BackButton/>
<div class="chosenCandidates">
    {#each $vote.candidate_ids as candidateId}
        <div class="chosenCandidate">
            <div class="name">{findCandidateById(candidates, candidateId).first_name + " " + findCandidateById(candidates, candidateId).last_name}</div>
            <div class="xButton" on:click={()=>switchCandidate(findCandidateById(candidates, candidateId)._id)}>&times;</div>
        </div>
    {/each}
    {#if $vote.candidate_ids.length === maxCandidates}
        <div class="candidateCount">Zvolili ste maximálny počet kandidátov</div>
    {:else}
        <div class="candidateCount">Ešte môžete zvoliť {maxCandidates - $vote.candidate_ids.length} kandidátov</div>
    {/if}
</div>


<h2>Kandidáti</h2>

<input type="text" id="search" placeholder="Vyhľadajte kandidáta" on:input={e => {
    paginationObject.currentPageNumber = 1
    paginationObject.searchTerm = e.target.value
    paginateCandidates(paginationObject)
}}>

<p><i>Kliknutím označte 5 poslancov, ktorých chcete voliť.</i></p>
<div class="candidates">
    <div>
        {#if paginatedCandidates.length === 0}
            <Warning text="Neboli nájdení kandidáti vyhovujúce vášmu vyhľadávaniu" />
        {:else}
            <div class="legend">
                <span>Meno</span>
                <span>Tituly</span>
                <span>Vek</span>
                <span>Povolanie</span>
                <span>Bydlisko</span>
            </div>
            {#each paginatedCandidates as candidate, index}
                <CandidateBox showCheckbox={true} candidate={candidate}
                              isSelected={$vote.candidate_ids.includes(candidate._id)}
                              on:click={()=>switchCandidate(candidate._id)}/>
            {/each}
        {/if}
    </div>
</div>
<PaginationLinks paginationObject={paginationObject} paginationObjectChanged={paginateCandidates}/>
<Button on:click={next} type="primary">Potvrdiť</Button>

<Modal bind:openModal={openErrorModal} yesTxt="Odoslať hlas" cancelTxt="Späť">
    <span slot="title">Už ste si zvolili 5 kandidátov</span>
    <span slot="subtitle">Je možné zvoliť iba maximálne {maxCandidates} kandidátov</span>
</Modal>