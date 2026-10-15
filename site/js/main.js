
function wb_form_validateForm(formId, values, errors) {
	var form = $("input[name='wb_form_id'][value='" + formId + "']").parent();
	if (!form || form.length === 0 || !errors) return;
	
	form.find("input[name],textarea[name]").css({backgroundColor: ""});
	
	if (errors.required) {
		for (var i = 0; i < errors.required.length; i++) {
			var name = errors.required[i];
			var elem = form.find("input[name='" + name + "'],textarea[name='" + name + "'],select[name='" + name + "']");
			elem.css({backgroundColor: "#ff8c8c"});
		}
	}
	
	if (Object.keys(errors).length) {
		for (var k in values) {
			var elem = form.find("input[name='" + k + "'],textarea[name='" + k + "'],select[name='" + k + "']");
			elem.val(values[k]);
		}
	}
}

$(function() {
	var comboBoxes = $('.wb-combobox-controll');
	if (comboBoxes.length) {
		comboBoxes.each(function() {
			var thisCombo = $(this);
			var clickFunc = function() {
				var w = thisCombo.find('input').outerWidth();
				var mw = (menu = thisCombo.find('.dropdown-menu')).width();
				var ew = thisCombo.parent().outerWidth();
				if (mw < ew) menu.width(ew);
				menu.css({ marginLeft: (-w) + 'px' });
				thisCombo.find('.btn-group').toggleClass('open');
			};
			$(this).find('input').bind('click', clickFunc);
			$(this).find('.dropdown-toggle').bind('click', clickFunc);
		});
		
		$(document).bind('click', function(e) {
			var t = $(e.target);
			if (!t.is('.wb-combobox-controll')) {
				t = t.parents('.wb-combobox-controll');
				$.each($('.wb-combobox-controll'), function() {
					if (t.get(0) !== $(this).get(0)) {
						$(this).find('.btn-group').removeClass('open');
					}
				});
			}
		});
	}
	if (currLang) {
		$('.lang-selector').each(function() {
			var thisElem = $(this);
			var type = thisElem.attr('data-type');
			if (type == 'flags') {
				thisElem.find('a[data-lang="' + currLang + '"]').addClass('active');
			} else if (type == 'select') {
				var actLi = thisElem.find('li[data-lang="' + currLang + '"]');
				actLi.addClass('active');
				thisElem.find('input').val(actLi.find('a').html());
			}
		});
	}
	$('.btn-group.dropdown').each(function() {
		var ddh = $(this).height();
		var ddm = $(this).children('.dropdown-menu');
		ddm.addClass('open');
		var ddmh = ddm.height();
		ddm.removeClass('open');
		var ddt = $(this).offset().top;
		var dh = $(document).height();
		if (ddt + ddh + ddmh + 2 >= dh) {
			$(this).removeClass('dropdown').addClass('dropup');
		}
	});
	
	if ($('.menu-landing').length) {
		var switchLandingPage = function(alias, scroll) {
			var anchor = $('.wb_page_anchor[name="' + alias + '"]');
			if (anchor.length) {
				if (scroll) {
					anchor.attr('name', '');
					setTimeout(function() {
						anchor.attr('name', alias);
					}, 10);
					$(window).unbind('scroll', windowScrollHandler);
					$('html, body').animate({ scrollTop: anchor.offset().top + 'px' }, 540, function() {
						$(window).bind('scroll', windowScrollHandler);
					});
				}
			}
			var item = $('.menu-landing li a[href="#' + alias + '"]').parent();
			if (item.length) {
				var items = item.parent().children('li');
				items.removeClass('active');
				item.addClass('active');
			}
		};
		var windowScrollHandler = function() {
			var anchors = $('.wb_page_anchor');
			$(anchors.get().reverse()).each(function() {
				if ($(this).offset().top <= $(window).scrollTop()) {
					var alias = $(this).attr('name');
					switchLandingPage(alias);
					return false;
				}
			});
		};
		$('.menu-landing li a').on('click', function(e) {
			var href = $(this).attr('href'), alias = href.substring(1);
			if (/^(?:http|https):\/\//.test(href)) return true;
			switchLandingPage(alias, true);
			window.history.pushState(null, null, (currLang ? currLang + '/' : '') + '#' + alias);
			e.preventDefault();
		});
		$(window).on('hashchange', function() {
			var link = $('.menu-landing li a[href="' + location.hash + '"]');
			if (link.length) {
				var item = link.parent();
				var items = item.parent().children('li');
				items.removeClass('active');
				item.addClass('active');
			}
		});
		$(window).bind('scroll', windowScrollHandler);
		$(window).trigger('hashchange');
	}
});
