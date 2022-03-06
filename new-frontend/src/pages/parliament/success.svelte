<script>
    import ImageScreen, {icons} from "../../lib/ImageScreen.svelte";
    import {goto} from "@roxi/routify";

    setTimeout(() => {
        $goto("/");
    }, 5000);

</script>

<ImageScreen icon={icons.SUCCESS} title="Váš hlas bol započítaný">
    Ďakujeme za vašu účasť
</ImageScreen>