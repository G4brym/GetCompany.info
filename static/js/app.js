! function(e) {
    "function" == typeof define && define.amd ? define(["jquery"], e) : e("object" == typeof exports ? require("jquery") : jQuery)
}(function(e) {
    function n(e) {
        return u.raw ? e : encodeURIComponent(e)
    }

    function o(e) {
        return u.raw ? e : decodeURIComponent(e)
    }

    function i(e) {
        return n(u.json ? JSON.stringify(e) : String(e))
    }

    function r(e) {
        0 === e.indexOf('"') && (e = e.slice(1, -1).replace(/\\"/g, '"').replace(/\\\\/g, "\\"));
        try {
            return e = decodeURIComponent(e.replace(c, " ")), u.json ? JSON.parse(e) : e
        } catch (n) {}
    }

    function t(n, o) {
        var i = u.raw ? n : r(n);
        return e.isFunction(o) ? o(i) : i
    }
    var c = /\+/g,
        u = e.cookie = function(r, c, f) {
            if (void 0 !== c && !e.isFunction(c)) {
                if (f = e.extend({}, u.defaults, f), "number" == typeof f.expires) {
                    var a = f.expires,
                        d = f.expires = new Date;
                    d.setTime(+d + 864e5 * a)
                }
                return document.cookie = [n(r), "=", i(c), f.expires ? "; expires=" + f.expires.toUTCString() : "", f.path ? "; path=" + f.path : "", f.domain ? "; domain=" + f.domain : "", f.secure ? "; secure" : ""].join("")
            }
            for (var p = r ? void 0 : {}, s = document.cookie ? document.cookie.split("; ") : [], m = 0, x = s.length; x > m; m++) {
                var v = s[m].split("="),
                    k = o(v.shift()),
                    l = v.join("=");
                if (r && r === k) {
                    p = t(l, c);
                    break
                }
                r || void 0 === (l = t(l)) || (p[k] = l)
            }
            return p
        };
    u.defaults = {}, e.removeCookie = function(n, o) {
        return void 0 === e.cookie(n) ? !1 : (e.cookie(n, "", e.extend({}, o, {
            expires: -1
        })), !e.cookie(n))
    }
});

function _init() {
    "use strict";
    $.AdminLTE.layout = {
        activate: function() {
            var a = this;
            a.fix(), a.fixSidebar(), $(window, ".wrapper").resize(function() {
                a.fix(), a.fixSidebar()
            })
        },
        fix: function() {
            var a = $(".main-header").outerHeight() + $(".main-footer").outerHeight(),
                b = $(window).height(),
                c = $(".sidebar").height();
            if ($("body").hasClass("fixed")) $(".content-wrapper, .right-side").css("min-height", b - $(".main-footer").outerHeight());
            else {
                var d;
                b >= c ? ($(".content-wrapper, .right-side").css("min-height", b - a), d = b - a) : ($(".content-wrapper, .right-side").css("min-height", c), d = c);
                var e = $($.AdminLTE.options.controlSidebarOptions.selector);
                "undefined" != typeof e && e.height() > d && $(".content-wrapper, .right-side").css("min-height", e.height())
            }
        },
        fixSidebar: function() {
            return $("body").hasClass("fixed") ? ("undefined" == typeof $.fn.slimScroll && window.console && window.console.error("Error: the fixed layout requires the slimscroll plugin!"), void($.AdminLTE.options.sidebarSlimScroll && "undefined" != typeof $.fn.slimScroll && ($(".sidebar").slimScroll({
                destroy: !0
            }).height("auto"), $(".sidebar").slimscroll({
                height: $(window).height() - $(".main-header").height() + "px",
                color: "rgba(0,0,0,0.2)",
                size: "3px"
            })))) : void("undefined" != typeof $.fn.slimScroll && $(".sidebar").slimScroll({
                destroy: !0
            }).height("auto"))
        }
    }, $.AdminLTE.pushMenu = {
        activate: function(a) {
            var b = $.AdminLTE.options.screenSizes;
            $(document).on("click", a, function(a) {
                a.preventDefault(), $(window).width() > b.sm - 1 ? $("body").hasClass("sidebar-collapse") ? $("body").removeClass("sidebar-collapse").trigger("expanded.pushMenu") : $("body").addClass("sidebar-collapse").trigger("collapsed.pushMenu") : $("body").hasClass("sidebar-open") ? $("body").removeClass("sidebar-open").removeClass("sidebar-collapse").trigger("collapsed.pushMenu") : $("body").addClass("sidebar-open").trigger("expanded.pushMenu")
            }), $(".content-wrapper").click(function() {
                $(window).width() <= b.sm - 1 && $("body").hasClass("sidebar-open") && $("body").removeClass("sidebar-open")
            }), ($.AdminLTE.options.sidebarExpandOnHover || $("body").hasClass("fixed") && $("body").hasClass("sidebar-mini")) && this.expandOnHover()
        },
        expandOnHover: function() {
            var a = this,
                b = $.AdminLTE.options.screenSizes.sm - 1;
            $(".main-sidebar").hover(function() {
                $("body").hasClass("sidebar-mini") && $("body").hasClass("sidebar-collapse") && $(window).width() > b && a.expand()
            }, function() {
                $("body").hasClass("sidebar-mini") && $("body").hasClass("sidebar-expanded-on-hover") && $(window).width() > b && a.collapse()
            })
        },
        expand: function() {
            $("body").removeClass("sidebar-collapse").addClass("sidebar-expanded-on-hover")
        },
        collapse: function() {
            $("body").hasClass("sidebar-expanded-on-hover") && $("body").removeClass("sidebar-expanded-on-hover").addClass("sidebar-collapse")
        }
    }, $.AdminLTE.tree = function(a) {
        var b = this,
            c = $.AdminLTE.options.animationSpeed;
        $(document).on("click", a + " li a", function(a) {
            var d = $(this),
                e = d.next();
            if (e.is(".treeview-menu") && e.is(":visible") && !$("body").hasClass("sidebar-collapse")) e.slideUp(c, function() {
                e.removeClass("menu-open")
            }), e.parent("li").removeClass("active");
            else if (e.is(".treeview-menu") && !e.is(":visible")) {
                var f = d.parents("ul").first(),
                    g = f.find("ul:visible").slideUp(c);
                g.removeClass("menu-open");
                var h = d.parent("li");
                e.slideDown(c, function() {
                    e.addClass("menu-open"), f.find("li.active").removeClass("active"), h.addClass("active"), b.layout.fix()
                })
            }
            e.is(".treeview-menu") && a.preventDefault()
        })
    }, $.AdminLTE.controlSidebar = {
        activate: function() {
            var a = this,
                b = $.AdminLTE.options.controlSidebarOptions,
                c = $(b.selector),
                d = $(b.toggleBtnSelector);
            d.on("click", function(d) {
                d.preventDefault(), c.hasClass("control-sidebar-open") || $("body").hasClass("control-sidebar-open") ? a.close(c, b.slide) : a.open(c, b.slide)
            });
            var e = $(".control-sidebar-bg");
            a._fix(e), $("body").hasClass("fixed") ? a._fixForFixed(c) : $(".content-wrapper, .right-side").height() < c.height() && a._fixForContent(c)
        },
        open: function(a, b) {
            b ? a.addClass("control-sidebar-open") : $("body").addClass("control-sidebar-open")
        },
        close: function(a, b) {
            b ? a.removeClass("control-sidebar-open") : $("body").removeClass("control-sidebar-open")
        },
        _fix: function(a) {
            var b = this;
            $("body").hasClass("layout-boxed") ? (a.css("position", "absolute"), a.height($(".wrapper").height()), $(window).resize(function() {
                b._fix(a)
            })) : a.css({
                position: "fixed",
                height: "auto"
            })
        },
        _fixForFixed: function(a) {
            a.css({
                position: "fixed",
                "max-height": "100%",
                overflow: "auto",
                "padding-bottom": "50px"
            })
        },
        _fixForContent: function(a) {
            $(".content-wrapper, .right-side").css("min-height", a.height())
        }
    }, $.AdminLTE.boxWidget = {
        selectors: $.AdminLTE.options.boxWidgetOptions.boxWidgetSelectors,
        icons: $.AdminLTE.options.boxWidgetOptions.boxWidgetIcons,
        animationSpeed: $.AdminLTE.options.animationSpeed,
        activate: function(a) {
            var b = this;
            a || (a = document), $(a).on("click", b.selectors.collapse, function(a) {
                a.preventDefault(), b.collapse($(this))
            }), $(a).on("click", b.selectors.remove, function(a) {
                a.preventDefault(), b.remove($(this))
            })
        },
        collapse: function(a) {
            var b = this,
                c = a.parents(".box").first(),
                d = c.find("> .box-body, > .box-footer, > form  >.box-body, > form > .box-footer");
            c.hasClass("collapsed-box") ? (a.children(":first").removeClass(b.icons.open).addClass(b.icons.collapse), d.slideDown(b.animationSpeed, function() {
                c.removeClass("collapsed-box")
            })) : (a.children(":first").removeClass(b.icons.collapse).addClass(b.icons.open), d.slideUp(b.animationSpeed, function() {
                c.addClass("collapsed-box")
            }))
        },
        remove: function(a) {
            var b = a.parents(".box").first();
            b.slideUp(this.animationSpeed)
        }
    }
}
if ("undefined" == typeof jQuery) throw new Error("AdminLTE requires jQuery");
$.AdminLTE = {}, $.AdminLTE.options = {
        navbarMenuSlimscroll: !0,
        navbarMenuSlimscrollWidth: "3px",
        navbarMenuHeight: "200px",
        animationSpeed: 500,
        sidebarToggleSelector: "[data-toggle='offcanvas']",
        sidebarPushMenu: !0,
        sidebarSlimScroll: !0,
        sidebarExpandOnHover: !1,
        enableBoxRefresh: !0,
        enableBSToppltip: !0,
        BSTooltipSelector: "[data-toggle='tooltip']",
        enableFastclick: !0,
        enableControlSidebar: !0,
        controlSidebarOptions: {
            toggleBtnSelector: "[data-toggle='control-sidebar']",
            selector: ".control-sidebar",
            slide: !0
        },
        enableBoxWidget: !0,
        boxWidgetOptions: {
            boxWidgetIcons: {
                collapse: "fa-minus",
                open: "fa-plus",
                remove: "fa-times"
            },
            boxWidgetSelectors: {
                remove: '[data-widget="remove"]',
                collapse: '[data-widget="collapse"]'
            }
        },
        directChat: {
            enable: !0,
            contactToggleSelector: '[data-widget="chat-pane-toggle"]'
        },
        colors: {
            lightBlue: "#3c8dbc",
            red: "#f56954",
            green: "#00a65a",
            aqua: "#00c0ef",
            yellow: "#f39c12",
            blue: "#0073b7",
            navy: "#001F3F",
            teal: "#39CCCC",
            olive: "#3D9970",
            lime: "#01FF70",
            orange: "#FF851B",
            fuchsia: "#F012BE",
            purple: "#8E24AA",
            maroon: "#D81B60",
            black: "#222222",
            gray: "#d2d6de"
        },
        screenSizes: {
            xs: 480,
            sm: 768,
            md: 992,
            lg: 1200
        }
    }, $(function() {
        "use strict";
        $("body").removeClass("hold-transition"), "undefined" != typeof AdminLTEOptions && $.extend(!0, $.AdminLTE.options, AdminLTEOptions);
        var a = $.AdminLTE.options;
        _init(), $.AdminLTE.layout.activate(), $.AdminLTE.tree(".sidebar"), a.enableControlSidebar && $.AdminLTE.controlSidebar.activate(), a.navbarMenuSlimscroll && "undefined" != typeof $.fn.slimscroll && $(".navbar .menu").slimscroll({
            height: a.navbarMenuHeight,
            alwaysVisible: !1,
            size: a.navbarMenuSlimscrollWidth
        }).css("width", "100%"), a.sidebarPushMenu && $.AdminLTE.pushMenu.activate(a.sidebarToggleSelector), a.enableBSToppltip && $("body").tooltip({
            selector: a.BSTooltipSelector
        }), a.enableBoxWidget && $.AdminLTE.boxWidget.activate(), a.enableFastclick && "undefined" != typeof FastClick && FastClick.attach(document.body), a.directChat.enable && $(document).on("click", a.directChat.contactToggleSelector, function() {
            var a = $(this).parents(".direct-chat").first();
            a.toggleClass("direct-chat-contacts-open")
        }), $('.btn-group[data-toggle="btn-toggle"]').each(function() {
            var a = $(this);
            $(this).find(".btn").on("click", function(b) {
                a.find(".btn.active").removeClass("active"), $(this).addClass("active"), b.preventDefault()
            })
        })
    }),
    function(a) {
        "use strict";
        a.fn.boxRefresh = function(b) {
            function c(a) {
                a.append(f), e.onLoadStart.call(a)
            }

            function d(a) {
                a.find(f).remove(), e.onLoadDone.call(a)
            }
            var e = a.extend({
                    trigger: ".refresh-btn",
                    source: "",
                    onLoadStart: function(a) {
                        return a
                    },
                    onLoadDone: function(a) {
                        return a
                    }
                }, b),
                f = a('<div class="overlay"><div class="fa fa-refresh fa-spin"></div></div>');
            return this.each(function() {
                if ("" === e.source) return void(window.console && window.console.log("Please specify a source first - boxRefresh()"));
                var b = a(this),
                    f = b.find(e.trigger).first();
                f.on("click", function(a) {
                    a.preventDefault(), c(b), b.find(".box-body").load(e.source, function() {
                        d(b)
                    })
                })
            })
        }
    }(jQuery),
    function(a) {
        "use strict";
        a.fn.activateBox = function() {
            a.AdminLTE.boxWidget.activate(this)
        }, a.fn.toggleBox = function() {
            var b = a(a.AdminLTE.boxWidget.selectors.collapse, this);
            a.AdminLTE.boxWidget.collapse(b)
        }, a.fn.removeBox = function() {
            var b = a(a.AdminLTE.boxWidget.selectors.remove, this);
            a.AdminLTE.boxWidget.remove(b)
        }
    }(jQuery),
    function(a) {
        "use strict";
        a.fn.todolist = function(b) {
            var c = a.extend({
                onCheck: function(a) {
                    return a
                },
                onUncheck: function(a) {
                    return a
                }
            }, b);
            return this.each(function() {
                "undefined" != typeof a.fn.iCheck ? (a("input", this).on("ifChecked", function() {
                    var b = a(this).parents("li").first();
                    b.toggleClass("done"), c.onCheck.call(b)
                }), a("input", this).on("ifUnchecked", function() {
                    var b = a(this).parents("li").first();
                    b.toggleClass("done"), c.onUncheck.call(b)
                })) : a("input", this).on("change", function() {
                    var b = a(this).parents("li").first();
                    b.toggleClass("done"), a("input", b).is(":checked") ? c.onCheck.call(b) : c.onUncheck.call(b)
                })
            })
        }
    }(jQuery);

function newError(msg) {
    new PNotify({
        title: 'Erro',
        text: msg,
        icon: 'fa fa-exclamation-triangle',
        type: 'error'
    });
}

function newSuccess(msg) {
    new PNotify({
        title: 'Sucesso',
        text: msg,
        icon: 'fa fa-check',
        type: 'success'
    });
}

var sidebar_clicked_with_search = false;

$("#toggle-sidebar").on( "click", function() {
    if (sidebar_clicked_with_search) {
        $('#helper-search').hide();
    }
});

$(document).ready(function() {
    $("#search-index-button").click(function() {
        $("#search").val($("#search-index").val());
        if ($("#search").val().toString().trim().length < 3) {
            newError("Introduza No Minimo 3 Caracters");
        } else {

            if (sidebar_clicked_with_search == false) {
                $('#helper-search').slideDown("medium");
                sidebar_clicked_with_search = true;
            }

            $("#search-display").html('\
                        <li class="header search-result">Pesquisa</li>\
                        <center>\
                            <br><br>\
                            <i class="fa fa-refresh fa-spin fa-3x" style="color: #ffffff;" aria-hidden="true"></i>\
                        </center>');

            $("#search-display").slideDown("medium");

            var data = {
                "q": $("#search").val()
            };

            $.ajax({
                type: "POST",
                data: data,
                url: "/v1/search/",
                dataType: 'json',
                beforeSend: function(xhr) {
                    xhr.setRequestHeader("X-CSRFToken", $.cookie("csrftoken"));
                },
                success: function(xhr) {
                    if (xhr.code == 200) {

                        var tmp = '<li class="header">Pesquisa</li>'

                        for (i = 0; i < xhr.data.length; i++) {

                            tmp += '  <li>\
                                  <a href="/' + xhr.data[i].identifier + '/" style="width: 230px; padding-top: 5px; padding-bottom: 2px;">\
                                      <div class="row">\
                                          <div class="col-md-12">\
                                              <i class="fa fa-chevron-right" style="width: 20px;"></i>\
                                              <span class="search-result-name">' + xhr.data[i].name + '</span>\
                                          </div>\
                                          <div class="col-md-12">\
                                              <small style="font-size: 85%; float:left; margin-bottom: 5px;"> ' + xhr.data[i].state + '</small>\
                                              <small style="font-size: 85%; float:right; margin-right: 10px; margin-bottom: 5px;"> ' + xhr.data[i].identifier + '</small>\
                                          </div>\
                                      </div>\
                                  </a>\
                              </li>'
                        }

                        $("#search-display").html(tmp);

                    } else {
                        console.log(xhr["error"]);
                        newError("Ocorreu um erro, tente mais tarde");
                    }
                },
                error: function(xhr) {
                    console.log(xhr);
                    if (xhr.responseJSON.code == 404) {

                        $("#search-display").html('<li class="header">Pesquisa</li>\
                            <li>\
                                <a style="width: 230px; padding-top: 5px; padding-bottom: 2px;">\
                                    <div class="row">\
                                        <div class="col-md-12">\
                                            <i class="fa fa-close" style="width: 20px;"></i>\
                                            <span class="search-result-name">Nenhum Resultado</span>\
                                        </div>\
                                    </div>\
                                </a>\
                            </li>');

                    } else {
                        console.log(xhr["error"]);
                        newError("Não foi possivel contactar o servidor, tente mais tarde");
                    }
                }
            });
        }

    });
    $("#search-button").click(function() {
        if ($("#search").val().toString().trim().length < 3) {
            newError("Introduza No Minimo 3 Caracters");
        } else {


            $("#search-display").html('\
                          <li class="header search-result">Pesquisa</li>\
                          <center>\
                              <br><br>\
                              <i class="fa fa-refresh fa-spin fa-3x" style="color: #ffffff;" aria-hidden="true"></i>\
                          </center>');

            $("#search-display").slideDown("medium");

            var data = {
                "q": $("#search").val()
            };

            $.ajax({
                type: "POST",
                data: data,
                url: "/v1/search/",
                dataType: 'json',
                beforeSend: function(xhr) {
                    xhr.setRequestHeader("X-CSRFToken", $.cookie("csrftoken"));
                },
                success: function(xhr) {
                    if (xhr.code == 200) {
                        var tmp = '<li class="header">Pesquisa</li>'

                        for (i = 0; i < xhr.data.length; i++) {

                            tmp += '  <li>\
                                  <a href="/' + xhr.data[i].identifier + '/" style="width: 230px; padding-top: 5px; padding-bottom: 2px;">\
                                      <div class="row">\
                                          <div class="col-md-12">\
                                              <i class="fa fa-chevron-right" style="width: 20px;"></i>\
                                              <span class="search-result-name">' + xhr.data[i].name + '</span>\
                                          </div>\
                                          <div class="col-md-12">\
                                              <small style="font-size: 85%; float:left; margin-bottom: 5px;"> ' + xhr.data[i].state + '</small>\
                                              <small style="font-size: 85%; float:right; margin-right: 10px; margin-bottom: 5px;"> ' + xhr.data[i].identifier + '</small>\
                                          </div>\
                                      </div>\
                                  </a>\
                              </li>'
                        }

                        $("#search-display").html(tmp);

                    } else {
                        console.log(xhr["error"]);
                        newError("Ocorreu um erro, tente mais tarde");
                    }
                },
                error: function(xhr) {
                    console.log(xhr);
                    if (xhr.responseJSON.code == 404) {

                        $("#search-display").html('<li class="header">Pesquisa</li>\
                            <li>\
                                <a style="width: 230px; padding-top: 5px; padding-bottom: 2px;">\
                                    <div class="row">\
                                        <div class="col-md-12">\
                                            <i class="fa fa-close" style="width: 20px;"></i>\
                                            <span class="search-result-name">Nenhum Resultado</span>\
                                        </div>\
                                    </div>\
                                </a>\
                            </li>');

                    } else {
                        console.log(xhr["error"]);
                        newError("Não foi possivel contactar o servidor, tente mais tarde");
                    }
                }
            });

        }


    });
});

function crawl(token) {
    $.ajax({
        type: "GET",
        data: {
            "token": token
        },
        url: "/v1/moreinfo/",
        dataType: 'json',
        beforeSend: function(xhr) {
            xhr.setRequestHeader("X-CSRFToken", $.cookie("csrftoken"));
        },
        success: function(xhr) {
            if (xhr.code == 200) {

                var tmp = '';

                if (xhr.data.address != null) {
                    tmp += '<dt>Morada</dt><dd>' + xhr.data.address + '</dd>';
                }
                if (xhr.data.address_l2 != null) {
                    tmp += '<dt></dt><dd>' + xhr.data.address_l2 + '</dd>';
                }
                if (xhr.data.phone != null) {
                    tmp += '<dt>Telefone</dt><dd>' + xhr.data.phone + '</dd>';
                }
                if (xhr.data.mobile != null) {
                    tmp += '<dt>Telemóvel</dt><dd>' + xhr.data.mobile + '</dd>';
                }
                if (xhr.data.fax != null) {
                    tmp += '<dt>Fax</dt><dd>' + xhr.data.fax + '</dd>';
                }
                if (xhr.data.email != null) {
                    tmp += '<dt>Email</dt><dd>' + xhr.data.email + '</dd>';
                }
                if (xhr.data.links == true) {
                    tmp += '<br><dt>Links</dt><dd>';

                    if (xhr.data.website != null) {
                        tmp += '<a class="btn btn-sm btn-social-icon btn-website" href="' + xhr.data.website + '" target="_blank"><i class="fa fa-home"></i></a>';
                    }

                    if (xhr.data.facebook != null) {
                        tmp += '<a class="btn btn-sm btn-social-icon btn-facebook" href="' + xhr.data.facebook + '" target="_blank"><i class="fa fa-facebook"></i></a>';
                    }

                    if (xhr.data.twitter != null) {
                        tmp += '<a class="btn btn-sm btn-social-icon btn-twitter" href="' + xhr.data.twitter + '" target="_blank"><i class="fa fa-twitter"></i></a>';
                    }

                    if (xhr.data.linkedin != null) {
                        tmp += '<a class="btn btn-sm btn-social-icon btn-linkedin" href="' + xhr.data.linkedin + '" target="_blank"><i class="fa fa-linkedin"></i></a>';
                    }

                    if (xhr.data.googleplus != null) {
                        tmp += '<a class="btn btn-sm btn-social-icon btn-google" href="' + xhr.data.googleplus + '" target="_blank"><i class="fa fa-google-plus"></i></a>';
                    }

                    tmp += '</dd>';
                }

                $("#comp-info").replaceWith(tmp);

                tmp2 = '';
                tmp3 = '';

                if (xhr.data.info == true) {

                    if (xhr.data.about != null) {
                        if (xhr.data.active_tab == 1) {
                            tmp2 += '<li class="active"><a href="#about" data-toggle="tab">Sobre a empresa</a></li>'
                            tmp3 += '<div class="tab-pane fade active in" id="about">' + xhr.data.about + '</div>'
                        } else {
                            tmp2 += '<li><a href="#about" data-toggle="tab">Sobre a empresa</a></li>'
                            tmp3 += '<div class="tab-pane fade" id="about">' + xhr.data.about + '</div>'
                        }
                    }

                    if (xhr.data.products != null) {
                        if (xhr.data.active_tab == 2) {
                            tmp2 += '<li class="active"><a href="#products" data-toggle="tab">Produtos e Serviços</a></li>'
                            tmp3 += '<div class="tab-pane fade active in" id="products">' + xhr.data.products + '</div>'
                        } else {
                            tmp2 += '<li><a href="#products" data-toggle="tab">Produtos e Serviços</a></li>'
                            tmp3 += '<div class="tab-pane fade" id="products">' + xhr.data.products + '</div>'
                        }
                    }

                    if (xhr.data.brands != null) {
                        if (xhr.data.active_tab == 3) {
                            tmp2 += '<li class="active"><a href="#brands" data-toggle="tab">Marcas</a></li>'
                            tmp3 += '<div class="tab-pane fade active in" id="brands">' + xhr.data.brands + '</div>'
                        } else {
                            tmp2 += '<li><a href="#brands" data-toggle="tab">Marcas</a></li>'
                            tmp3 += '<div class="tab-pane fade" id="brands">' + xhr.data.brands + '</div>'
                        }
                    }

                    if (xhr.data.tagss != null) {
                        if (xhr.data.active_tab == 4) {
                            tmp2 += '<li class="active"><a href="#tags" data-toggle="tab">Tags</a></li>'
                            tmp3 += '<div class="tab-pane fade active in" id="tags">' + xhr.data.tagss + '</div>'
                        } else {
                            tmp2 += '<li><a href="#tags" data-toggle="tab">Tags</a></li>'
                            tmp3 += '<div class="tab-pane fade" id="tags">' + xhr.data.tagss + '</div>'
                        }
                    }

                }

                if (xhr.data.cae_text != null) {
                    $("#cae_text").replaceWith("<dt></dt><dd>" + xhr.data.cae_text + "</dd>");
                }

                $("#comp-about-tiles").html(tmp2);
                $("#comp-about-content").html(tmp3);
                $("#comp-about-div").slideDown("medium");




            } else {
                console.log(xhr["error"]);
                newError("Ocorreu um erro, tente mais tarde");
            }
        },
        error: function(xhr) {
            console.log(xhr);

            if (xhr.code == 400) {
                console.log(xhr["error"]);
                newError("Não foi possivel contactar o servidor, tente mais tarde");

            } else {
                console.log(xhr["error"]);
                newError("Não foi possivel contactar o servidor, tente mais tarde");
            }
        }
    });
}