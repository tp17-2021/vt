<script>
    import {enToSkPaths} from "../../translations/paths";
    import {page, url, metatags} from '@roxi/routify'



    // example of paths array: ['home', 'nfc', 'add']
    let paths = []

    function updatePaths(pathname) {
        paths = pathname.split('/')

        paths = paths.filter(path => {
                return !["", "admin-frontend", "gateway", "index", "idle", "error", "success", "off"].includes(path);
            }
        )

        // set title to last path in paths array
        if (paths.length > 0) {
            let lastPath = paths[paths.length - 1]
            let title = enToSkPaths[lastPath]
            if (title) {
                metatags.title = title + " | Volebný terminál"
            }
        }
        else {
            metatags.title = 'Volebný terminál'
        }

        console.log(paths, $page);
    }


    // translate path to slovak if slovak translation exists
    function getTranslation(path) {
        return enToSkPaths[path] || path;
    }

    $: updatePaths($page.path);
</script>
<style lang="scss">
  @import 'node_modules/@id-sk/frontend/govuk/components/breadcrumbs/_breadcrumbs.scss';
</style>


<div class="govuk-breadcrumbs">
    <ol class="govuk-breadcrumbs__list">
        {#each paths as path, index }
            <!-- if not last-->
            {#if paths.length !== index  + 1}
                <li class="govuk-breadcrumbs__list-item">
                    <a class="govuk-breadcrumbs__link" href={$url("/" + paths.slice(0, index + 1).join("/"))}>{getTranslation(path)}</a>
                </li>
            {:else}
                <li class="govuk-breadcrumbs__list-item">
                    {getTranslation(path)}
                </li>
            {/if}
        {/each}
    </ol>
</div>