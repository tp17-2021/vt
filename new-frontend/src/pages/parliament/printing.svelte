<script>
    import { sendVoteParliament } from "../../api/rest";
    import { goto } from "@roxi/routify";

    import { onMount } from "svelte";

    import ImageScreen, { icons } from "../../lib/ImageScreen.svelte";

    onMount(() => {
        sendVoteParliament()
            .then(() => {
                // will be sent as a WS message from the server to switch to success message
            })
            .catch(() => {
                
                $goto("/parliament/error");
            });
    });

</script>

<ImageScreen icon={icons.SPINNER} title="Tlačíme váš lístok">
    Čakajte prosím
</ImageScreen>
