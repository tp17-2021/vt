<script>
    import {navigateTo} from "svelte-router-spa";

    let time = 2;  // prevent infinite loop
    const decTime = () => {
        time--;
        if (time > 0) {
            setTimeout(decTime, 1000);
        } else {
            navigateTo("/")
        }
    }
    decTime()
</script>

<h1>404 - stránka nenájdená</h1>
<p>Za {time} sekúnd budete presmerovaný na /</p>