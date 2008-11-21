

		$(function () {
			// Example 1
			$('form.signup input:text').magicpreview('mp_');

			// Example 2
			$('form.signup :text').magicpreview('p_');
			$('form.signup textarea').magicpreview('p_');
			$('form.signup  select').magicpreview('p_');


			$('form.photopreview select').magicpreview('img_', {
				'child': 'img',
				'change': 'src',
				'formatValue': function (value) { 
					return '/magicpreview/images/' + value + '.jpg'
				}
			});
		});



