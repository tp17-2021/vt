<script>
    import Button from "../../lib/components/buttons/Button.svelte";
    import {goto} from "@roxi/routify";
    import {vote} from "../../api/stores";
    import {sendVoteParliament} from "../../api/rest";

    function confirm() {
        sendVoteParliament()
            .then(() => {
                $goto("/");
            })
            .catch(() => {
                alert("Vyskytla se chyba při odoslan hlasu");
                $goto("/");
            });
    }

</script>

<h2>Potvrdenie voľby</h2>

<pre>
    {JSON.stringify($vote, null, 2)}
</pre>

<Button on:click={confirm}>Odoslať hlas</Button>
