"use strict";(self.webpackChunkpyams_app_msc=self.webpackChunkpyams_app_msc||[]).push([[137],{9137:(t,e,a)=>{a.r(e),a.d(e,{default:()=>d}),a(4061),a(960),a(6495),a(8255);var n=a(3830),s=a(4692);function r(t,e){var a="undefined"!=typeof Symbol&&t[Symbol.iterator]||t["@@iterator"];if(!a){if(Array.isArray(t)||(a=function(t,e){if(t){if("string"==typeof t)return i(t,e);var a={}.toString.call(t).slice(8,-1);return"Object"===a&&t.constructor&&(a=t.constructor.name),"Map"===a||"Set"===a?Array.from(t):"Arguments"===a||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(a)?i(t,e):void 0}}(t))||e&&t&&"number"==typeof t.length){a&&(t=a);var n=0,s=function(){};return{s,n:function(){return n>=t.length?{done:!0}:{done:!1,value:t[n++]}},e:function(t){throw t},f:s}}throw new TypeError("Invalid attempt to iterate non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}var r,o=!0,l=!1;return{s:function(){a=a.call(t)},n:function(){var t=a.next();return o=t.done,t},e:function(t){l=!0,r=t},f:function(){try{o||null==a.return||a.return()}finally{if(l)throw r}}}}function i(t,e){(null==e||e>t.length)&&(e=t.length);for(var a=0,n=Array(e);a<e;a++)n[a]=t[a];return n}var o=s.templates({markup:'\n\t<div class="alert alert-{{:status}}" role="alert">\n\t\t<button type="button" class="close" data-dismiss="alert" \n\t\t\t\taria-label="{{*: MyAMS.i18n.BTN_CLOSE }}">\n\t\t\t<i class="fa fa-times" aria-hidden="true"></i>\n\t\t</button>\n\t\t{{if header}}\n\t\t<h5 class="alert-heading">{{:header}}</h5>\n\t\t{{/if}}\n\t\t{{if message}}\n\t\t<p>{{:message}}</p>\n\t\t{{/if}}\n\t\t{{if messages}}\n\t\t<ul>\n\t\t{{for messages}}\n\t\t\t<li>\n\t\t\t\t{{if header}}<strong>{{:header}} :</strong>{{/if}}\n\t\t\t\t{{:message}}\n\t\t\t</li>\n\t\t{{/for}}\n\t\t</ul>\n\t\t{{/if}}\n\t\t{{if widgets}}\n\t\t<ul>\n\t\t{{for widgets}}\n\t\t\t<li>\n\t\t\t\t{{if header}}<strong>{{:header}} :</strong>{{/if}}\n\t\t\t\t{{:message}}\n\t\t\t</li>\n\t\t{{/for}}\n\t\t</ul>\n\t\t{{/if}}\n\t</div>',allowCode:!0}),l=function(t){s(".alert-success, SPAN.state-success",t).not(".persistent").remove(),s(".state-success",t).removeClassPrefix("state-"),s(".invalid-feedback",t).remove(),s(".is-invalid",t).removeClass("is-invalid")},c=function(t){s(".alert-danger, SPAN.state-error",t).not(".persistent").remove(),s(".state-error",t).removeClassPrefix("state-"),s(".invalid-feedback",t).remove(),s(".is-invalid",t).removeClass("is-invalid")},m={init:function(t){s("label",t).removeClass("col-md-3"),s(".col-md-9",t).removeClass("col-md-9"),s("input, select, textarea",t).addClass("form-control"),s("button",t).addClass("border"),s('button[type="submit"]',t).addClass("btn-primary");var e=s("html").attr("lang"),r=s("input[data-input-mask]");r.length>0&&a.e(660).then(a.t.bind(a,1660,23)).then((function(){r.each((function(t,e){var a=s(e),n=a.data(),r=s.extend({},{autoUnmask:!0,clearIncomplete:!0,removeMaskOnSubmit:!0},n.amsInputMaskOptions||n.amsOptions||n.options),i={veto:!1};if(a.trigger("before-init.ams.inputmask",[a,r,i]),!i.veto){var o=new Inputmask(n.inputMask,r).mask(e);a.trigger("after-init.ams.inputmask",[a,o])}}))}));var i=s(".select2");i.length>0&&a.e(458).then(a.t.bind(a,5458,23)).then((function(){i.each((function(t,a){var r=s(a),i=r.data(),o={theme:i.amsSelect2Options||i.amsTheme||"bootstrap",language:i.amsSelect2Language||i.amsLanguage||e};if(i.amsSelect2AjaxUrl||i.amsAjaxUrl||i["ajax-Url"]){var l,c=n.A.getFunctionByName(i.amsSelect2AjaxParams||i.amsAjaxParams||i["ajax-Params"])||i.amsSelect2AjaxParams||i.amsAjaxParams||i["ajax-Params"];"function"==typeof c?l=c:c&&(l=function(t){return _select2Helpers.select2AjaxParamsHelper(t,c)}),o.ajax={url:n.A.getFunctionByName(i.amsSelect2AjaxUrl||i.amsAjaxUrl)||i.amsSelect2AjaxUrl||i.amsAjaxUrl,data:l||n.A.getFunctionByName(i.amsSelect2AjaxData||i.amsAjaxData)||i.amsSelect2AjaxData||i.amsAjaxData,processResults:n.A.getFunctionByName(i.amsSelect2AjaxProcessResults||i.amsAjaxProcessResults)||i.amsSelect2AjaxProcessResults||i.amsAjaxProcessResults,transport:n.A.getFunctionByName(i.amsSelect2AjaxTransport||i.amsAjaxTransport)||i.amsSelect2AjaxTransport||i.amsAjaxTransport},o.minimumInputLength=i.amsSelect2MinimumInputLength||i.amsMinimumInputLength||i.minimumInputLength||1}var m=s.extend({},o,i.amsSelect2Options||i.amsOptions||i.options),d={veto:!1};if(r.trigger("before-init.ams.select2",[r,m,d]),!d.veto){var u=r.select2(m);r.trigger("after-init.ams.select2",[r,u])}}))}));var o=s(".datetime");o.length>0&&a.e(624).then(a.t.bind(a,6624,23)).then((function(){o.each((function(t,a){var n=s(a),r=n.data(),i={locale:r.amsDatetimeLanguage||r.amsLanguage||e,icons:{time:"far fa-clock",date:"far fa-calendar",up:"fas fa-arrow-up",down:"fas fa-arrow-down",previous:"fas fa-chevron-left",next:"fas fa-chevron-right",today:"far fa-calendar-check-o",clear:"far fa-trash",close:"far fa-times"},date:n.val()||a.defaultValue,format:r.amsDatetimeFormat||r.amsFormat},o=s.extend({},i,r.datetimeOptions||r.options),l={veto:!1};if(n.trigger("before-init.ams.datetime",[n,o,l]),!l.veto){n.datetimepicker(o);var c=n.data("datetimepicker");(r.amsDatetimeIsoTarget||r.amsIsoTarget)&&n.on("change.datetimepicker",(function(t){var e=s(t.currentTarget).data();s(e.amsDatetimeIsoTarget||e.amsIsoTarget).val(t.date?t.date.toISOString(!0):null)})),n.trigger("after-init.ams.datetime",[n,c])}}))}));var l={submitHandler:m.submitHandler,messages:{}},c=function(){s(t).each((function(t,e){var a=s.extend({},l);s(e).validate(function(t,e){return s("[data-ams-validate-messages]",t).each((function(t,a){e.messages[s(a).attr("name")]=s(a).data("ams-validate-messages"),e.errorClass="error d-block",e.errorPlacement=function(t,e){e.parents("div:first").append(t)}})),e}(e,a))}))};"fr"===e?a.e(47).then(a.t.bind(a,3047,23)).then((function(){c()})):c()},showMessage:function(t,e){var a;l(e),c(e),a={status:"success",header:t.header||n.A.i18n.SUCCESS,message:t.message||null},s(o.render(a)).prependTo(e),s.scrollTo(".alert",{offset:-15})},showErrors:function(t,e){var a=function(t,e,a){if("string"==typeof e&&(e=s('[name="'.concat(e,'"]'),t)),e.exists()){var n=e.closest(".form-widget");s(".invalid-feedback",n).remove(),s("<span>").text(a).addClass("is-invalid invalid-feedback").appendTo(n),e.removeClass("valid").addClass("is-invalid")}};l(e),c(e),function(){var i,l=[],c=r(t.messages||[]);try{for(c.s();!(i=c.n()).done;){var m=i.value;"string"==typeof m?l.push({header:null,message:m}):l.push(m)}}catch(t){c.e(t)}finally{c.f()}var d,u=r(t.widgets||[]);try{for(u.s();!(d=u.n()).done;){var f=d.value;l.push({header:f.label,message:f.message})}}catch(t){u.e(t)}finally{u.f()}var p={status:"danger",header:t.header||(l.length>1?n.A.i18n.ERRORS_OCCURRED:n.A.i18n.ERROR_OCCURRED),message:t.error||null,messages:l};s(o.render(p)).prependTo(e);var v,g=r(t.widgets||[]);try{for(g.s();!(v=g.n()).done;){var h=v.value,b=void 0;(b=h.id?s("#".concat(h.id),e):s('[name="'.concat(h.name,'"]'),e)).exists()&&a(e,b,h.message),b.parents("fieldset.switched").each((function(t,e){s("legend.switcher",e).click()})),b.parents(".tab-pane").each((function(t,e){var a=s(e),n=a.parents(".tab-content").siblings(".nav-tabs");s("li:nth-child(".concat(a.index()+1,")"),n).addClass("is-invalid"),s("li.is-invalid:first a",n).click()}))}}catch(t){g.e(t)}finally{g.f()}}(),s.scrollTo(".alert",{offset:-15})},submitHandler:function(t){var e=function(t){var e=s('button[type="submit"]',t),a=e.attr("name"),r=s('input[name="'+a+'"]',t);0===r.length?s("<input />").attr("type","hidden").attr("name",a).attr("value",e.attr("value")).appendTo(t):r.val(e.attr("value"));var i=s("meta[name=csrf-param]").attr("content"),l=s("meta[name=csrf-token]").attr("content"),d=s('input[name="'.concat(i,'"]'),t);0===d.length?s("<input />").attr("type","hidden").attr("name",i).attr("value",l).appendTo(t):d.val(l),s(t).ajaxSubmit({success:function(t,e,a,n){var r=a.getResponseHeader("content-type");if("application/json"===r){var i=t.status;switch(i){case"success":m.showMessage(t,n);break;case"error":m.showErrors(t,n);break;case"reload":case"redirect":var o=t.location;window.location.href===o?window.location.reload():window.location.replace(o);break;default:window.console&&(window.console.warn("Unhandled JSON status: ".concat(i)),window.console.warn(" > ".concat(t)))}}else"text/html"===r&&s("#main").html(t)},error:function(t,e,a,r){c(r);var i={status:"danger",header:n.A.i18n.ERROR_OCCURRED,message:a};s(o.render(i)).prependTo(r),s.scrollTo(".alert",{offset:-15})}})};if(window.grecaptcha){var a=s(t).data("ams-form-captcha-key");grecaptcha.execute(a,{action:"form_submit"}).then((function(a){s(".state-error",t).removeClass("state-error"),s('input[name="g-recaptcha-response"]',t).val(a),e(t)}))}else e(t)}};const d=m}}]);