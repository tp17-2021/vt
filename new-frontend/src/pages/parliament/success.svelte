<script>
    import ImageScreen, {icons} from "../../lib/ImageScreen.svelte";

    // status will be automatically changed using websocket from backend to electionStatus.WAITING_FOR_NFC_TAG to switch back to /
</script>

<ImageScreen icon={icons.SUCCESS} title="Váš hlas bol započítaný">
    Ďakujeme za vašu účasť
</ImageScreen>