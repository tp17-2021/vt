<script>
    import Button from "../../lib/components/buttons/Button.svelte";
    import {goto} from "@roxi/routify";
    import {vote} from "../../api/stores";
    import CandidateBox from "../../lib/components/CandidateBox.svelte";
    import PartyBox from "../../lib/components/PartyBox.svelte";
    import {findCandidateById, findPartyById} from "../../lib/helpers";
    import Warning from "../../lib/components/Warning.svelte";
    import BackButton from "../../lib/components/buttons/BackButton.svelte";
    import ButtonsContainer from "../../lib/components/buttons/ButtonsContainer.svelte";

    async function confirm() {
        $goto("/parliament/printing");
    }

    function changeVote() {
        $goto("/parliament/party");
    }

    const party = findPartyById($vote.party_id)
    console.log("party", party)
</script>

<style>
    .chosen-candidates {
        margin-bottom: 1rem;
    }
    .cancelYes {
        margin-top: 2rem;
        display: flex;
        justify-content: end;
        gap: 1rem;
    }
</style>

<BackButton/>
<h2>Potvrdenie voľby</h2>
<h2>Zvolená strana</h2>
{#if $vote.party_id === null}
    <Warning text="Nezvolili ste žiadnu politickú stranu"/>
{:else}
    <PartyBox {party}/>
{/if}

<h2 class="mt-3">Zvolení kandidáti na poslancov</h2>
<div class="chosen-candidates">
    {#if $vote.candidate_ids.length === 0}
        <Warning text="Nezvolili ste žiadneho kandidáta"/>
    {/if}
    {#each $vote.candidate_ids as candidate_id}
        <CandidateBox candidate={findCandidateById(party.candidates, candidate_id)}/>
    {/each}
</div>

<div class="cancelYes">
    <Button on:click={changeVote}>Chcem upraviť svoju voľbu</Button>
    <Button on:click={confirm} type="primary">Odoslať hlas</Button>
</div>
<ButtonsContainer>

</ButtonsContainer>


