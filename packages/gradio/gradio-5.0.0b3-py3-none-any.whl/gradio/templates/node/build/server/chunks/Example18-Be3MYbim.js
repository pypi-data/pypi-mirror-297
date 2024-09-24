import { c as create_ssr_component, b as add_attribute, e as escape, f as each, v as validate_component } from './ssr-Cz1f32Mr.js';
import { I as Image$1 } from './Image2-CIpzhHTx.js';
import './2-DleTh3G7.js';
import { V as Video } from './Video2-CDNDBnbJ.js';
import './file-url-D-K40zdU.js';
import './index4-D_FyJKAV.js';
import './hls-CrxM9YLy.js';

const css = {
  code: ".gallery.svelte-glyrxt{padding:var(--size-1) var(--size-2);display:flex;align-items:center;gap:20px;overflow-x:auto}div.svelte-glyrxt{overflow:hidden;min-width:var(--local-text-width);white-space:nowrap}.container.svelte-glyrxt img,.container.svelte-glyrxt video{object-fit:contain;width:100px;height:100px}.container.selected.svelte-glyrxt{border-color:var(--border-color-accent)}.border.table.svelte-glyrxt{border:2px solid var(--border-color-primary)}.container.table.svelte-glyrxt{margin:0 auto;border-radius:var(--radius-lg);overflow-x:auto;width:max-content;height:max-content;object-fit:cover;padding:var(--size-2)}.container.gallery.svelte-glyrxt{object-fit:cover}div.svelte-glyrxt>p{font-size:var(--text-lg);white-space:normal}",
  map: '{"version":3,"file":"Example.svelte","sources":["Example.svelte"],"sourcesContent":["<script lang=\\"ts\\">import { onMount } from \\"svelte\\";\\nimport { Image } from \\"@gradio/image/shared\\";\\nimport { Video } from \\"@gradio/video/shared\\";\\nexport let value = {\\n  text: \\"\\",\\n  files: []\\n};\\nexport let type;\\nexport let selected = false;\\nlet size;\\nlet el;\\nfunction set_styles(element, el_width) {\\n  if (!element || !el_width)\\n    return;\\n  el.style.setProperty(\\n    \\"--local-text-width\\",\\n    `${el_width < 150 ? el_width : 200}px`\\n  );\\n  el.style.whiteSpace = \\"unset\\";\\n}\\nonMount(() => {\\n  set_styles(el, size);\\n});\\n<\/script>\\n\\n<div\\n\\tclass=\\"container\\"\\n\\tbind:clientWidth={size}\\n\\tbind:this={el}\\n\\tclass:table={type === \\"table\\"}\\n\\tclass:gallery={type === \\"gallery\\"}\\n\\tclass:selected\\n\\tclass:border={value}\\n>\\n\\t<p>{value.text ? value.text : \\"\\"}</p>\\n\\t{#each value.files as file}\\n\\t\\t{#if file.mime_type && file.mime_type.includes(\\"image\\")}\\n\\t\\t\\t<Image src={file.url} alt=\\"\\" />\\n\\t\\t{:else if file.mime_type && file.mime_type.includes(\\"video\\")}\\n\\t\\t\\t<Video src={file.url} alt=\\"\\" loop={true} is_stream={false} />\\n\\t\\t{:else if file.mime_type && file.mime_type.includes(\\"audio\\")}\\n\\t\\t\\t<audio src={file.url} controls />\\n\\t\\t{:else}\\n\\t\\t\\t{file.orig_name}\\n\\t\\t{/if}\\n\\t{/each}\\n</div>\\n\\n<style>\\n\\t.gallery {\\n\\t\\tpadding: var(--size-1) var(--size-2);\\n\\t\\tdisplay: flex;\\n\\t\\talign-items: center;\\n\\t\\tgap: 20px;\\n\\t\\toverflow-x: auto;\\n\\t}\\n\\n\\tdiv {\\n\\t\\toverflow: hidden;\\n\\t\\tmin-width: var(--local-text-width);\\n\\t\\twhite-space: nowrap;\\n\\t}\\n\\n\\t.container :global(img),\\n\\t.container :global(video) {\\n\\t\\tobject-fit: contain;\\n\\t\\twidth: 100px;\\n\\t\\theight: 100px;\\n\\t}\\n\\n\\t.container.selected {\\n\\t\\tborder-color: var(--border-color-accent);\\n\\t}\\n\\t.border.table {\\n\\t\\tborder: 2px solid var(--border-color-primary);\\n\\t}\\n\\n\\t.container.table {\\n\\t\\tmargin: 0 auto;\\n\\t\\tborder-radius: var(--radius-lg);\\n\\t\\toverflow-x: auto;\\n\\t\\twidth: max-content;\\n\\t\\theight: max-content;\\n\\t\\tobject-fit: cover;\\n\\t\\tpadding: var(--size-2);\\n\\t}\\n\\n\\t.container.gallery {\\n\\t\\tobject-fit: cover;\\n\\t}\\n\\n\\tdiv > :global(p) {\\n\\t\\tfont-size: var(--text-lg);\\n\\t\\twhite-space: normal;\\n\\t}\\n</style>\\n"],"names":[],"mappings":"AAiDC,sBAAS,CACR,OAAO,CAAE,IAAI,QAAQ,CAAC,CAAC,IAAI,QAAQ,CAAC,CACpC,OAAO,CAAE,IAAI,CACb,WAAW,CAAE,MAAM,CACnB,GAAG,CAAE,IAAI,CACT,UAAU,CAAE,IACb,CAEA,iBAAI,CACH,QAAQ,CAAE,MAAM,CAChB,SAAS,CAAE,IAAI,kBAAkB,CAAC,CAClC,WAAW,CAAE,MACd,CAEA,wBAAU,CAAS,GAAI,CACvB,wBAAU,CAAS,KAAO,CACzB,UAAU,CAAE,OAAO,CACnB,KAAK,CAAE,KAAK,CACZ,MAAM,CAAE,KACT,CAEA,UAAU,uBAAU,CACnB,YAAY,CAAE,IAAI,qBAAqB,CACxC,CACA,OAAO,oBAAO,CACb,MAAM,CAAE,GAAG,CAAC,KAAK,CAAC,IAAI,sBAAsB,CAC7C,CAEA,UAAU,oBAAO,CAChB,MAAM,CAAE,CAAC,CAAC,IAAI,CACd,aAAa,CAAE,IAAI,WAAW,CAAC,CAC/B,UAAU,CAAE,IAAI,CAChB,KAAK,CAAE,WAAW,CAClB,MAAM,CAAE,WAAW,CACnB,UAAU,CAAE,KAAK,CACjB,OAAO,CAAE,IAAI,QAAQ,CACtB,CAEA,UAAU,sBAAS,CAClB,UAAU,CAAE,KACb,CAEA,iBAAG,CAAW,CAAG,CAChB,SAAS,CAAE,IAAI,SAAS,CAAC,CACzB,WAAW,CAAE,MACd"}'
};
const Example = create_ssr_component(($$result, $$props, $$bindings, slots) => {
  let { value = { text: "", files: [] } } = $$props;
  let { type } = $$props;
  let { selected = false } = $$props;
  let el;
  if ($$props.value === void 0 && $$bindings.value && value !== void 0)
    $$bindings.value(value);
  if ($$props.type === void 0 && $$bindings.type && type !== void 0)
    $$bindings.type(type);
  if ($$props.selected === void 0 && $$bindings.selected && selected !== void 0)
    $$bindings.selected(selected);
  $$result.css.add(css);
  return `<div class="${[
    "container svelte-glyrxt",
    (type === "table" ? "table" : "") + " " + (type === "gallery" ? "gallery" : "") + " " + (selected ? "selected" : "") + " " + (value ? "border" : "")
  ].join(" ").trim()}"${add_attribute("this", el, 0)}><p>${escape(value.text ? value.text : "")}</p> ${each(value.files, (file) => {
    return `${file.mime_type && file.mime_type.includes("image") ? `${validate_component(Image$1, "Image").$$render($$result, { src: file.url, alt: "" }, {}, {})}` : `${file.mime_type && file.mime_type.includes("video") ? `${validate_component(Video, "Video").$$render(
      $$result,
      {
        src: file.url,
        alt: "",
        loop: true,
        is_stream: false
      },
      {},
      {}
    )}` : `${file.mime_type && file.mime_type.includes("audio") ? `<audio${add_attribute("src", file.url, 0)} controls></audio>` : `${escape(file.orig_name)}`}`}`}`;
  })} </div>`;
});

export { Example as default };
//# sourceMappingURL=Example18-Be3MYbim.js.map
