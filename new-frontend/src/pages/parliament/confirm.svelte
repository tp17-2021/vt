<script>
    import Button from "../../lib/components/buttons/Button.svelte";
    import {goto} from "@roxi/routify";
    import {vote} from "../../api/stores";
    import {sendVoteParliament} from "../../api/rest";
    import CandidateBox from "../../lib/components/CandidateBox.svelte";
    import PartyBox from "../../lib/components/PartyBox.svelte";
    import {findCandidateById, findCandidatesByPartyId, findPartyById} from "../../lib/helpers";
    import Warning from "../../lib/components/Warning.svelte";
    import BackButton from "../../lib/components/buttons/BackButton.svelte";

    function confirm() {
        sendVoteParliament()
            .then(() => {
                $goto("/parliament/success");
            })
            .catch(() => {
                // alert("Vyskytla sa chyba pri odoslaní hlasu");
                $goto("/parliament/error");
            });
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
    {#if $vote.candidates_ids.length === 0}
        <Warning text="Nezvolili ste žiadneho kandidáta"/>
    {/if}
    {#each $vote.candidates_ids as candidate_id}
        <CandidateBox candidate={findCandidateById(party.candidates, candidate_id)}/>
    {/each}
</div>

<Button on:click={confirm} type="primary">Odoslať hlas</Button>
<Button on:click={changeVote}>Chcem upraviť svoju voľbu</Button>

<pre>
    {JSON.stringify($vote, null, 2)}
</pre>



