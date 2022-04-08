<script>
    import ImageScreen, {icons} from "../lib/ImageScreen.svelte";
    import Button from "../lib/components/buttons/Button.svelte";
    import {goto} from "@roxi/routify";

    function next() {
        $goto("/home/nfc/add/");
    }
</script>

<ImageScreen icon={icons.ERROR} title="Nie sú spustené voľby"></ImageScreen>