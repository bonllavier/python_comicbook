$(document).ready(function () {
			$('#loading').hide();
			$('#list').on('click', function () {
				console.log("list");
				$('#products .item').addClass('list-group-item');
				$('#products .card_comic_img').addClass('img-fluid');
			});
			$('#grid').on('click', function () {	
				console.log("grid");
				$('#products .item').removeClass('list-group-item');
				$('#products .card_comic_img').removeClass('img-fluid');
				$('#products .item').addClass('grid-group-item');
			});
			$('#next_page').on('click', function () {	
				console.log("pressed next page");
				let tmp_url = window.location.toString()
				console.log(tmp_url.split("/"))
				let actual_index = tmp_url[tmp_url.length - 1]
				try {
					let tmp_int = parseInt(actual_index)
					if (tmp_int >= 0)
					{
						$('#loading').show();
						console.log("act index", actual_index);
						window.location.replace(window.location.origin + '/' + (parseInt(actual_index) + 1).toString());
					}
					else{
						$('#loading').show();
						console.log("else");
						window.location.replace(window.location.origin + '/' + '1');
					}
				}
				catch(error) {
					$('#loading').show();
					console.log("ctach");
					window.location.replace(window.location.origin + '/' + '1');
				}
			});
			
			$('.comic_item').on('click', function () {	
				console.log($(this).attr('name'));
				$('#loading').show();
				window.location.replace(window.location.origin + '/issue/' + $(this).attr('name'));
			});

			

});