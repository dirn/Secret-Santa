!function($) {
    var $window = $(window);
    var $body = $(document.body);

    var navHeight = $('.navbar').outerHeight(true) + 10;

    $body.scrollspy({
      target: '.xmas-sidebar',
      offset: navHeight
    });

    $window.on('load', function () {
      $body.scrollspy('refresh');
    });

    $('.xmas-container [href=#]').click(function(e) {
        e.preventDefault();
    });

    setTimeout(function () {
      var $sidebar = $('.xmas-sidebar');

      $sidebar.affix({
        offset: {
          top: function () {
            var offsetTop = $sidebar.offset().top;
            var sidebarMargin = parseInt($sidebar.children(0).css('margin-top'), 10);
            var navOuterHeight = $('.xmas-main-nav').height();

            return (this.top = offsetTop - navOuterHeight - sidebarMargin);
          }
        }
      });
    }, 100);

    setTimeout(function () {
      $('.xmas-top').affix();
    }, 100);

    $('.xmas-section').on('click', 'button', function() {
        var $this = $(this);
        var id = $this.data('id');
        var quantity= 1;

        var url = '', method = 'POST';
        if ($this.hasClass('xmas-claim')) {
            url = '/claim';

            var $quantity= $this.closest('.xmas-details').find('input[name=quantity]');
            if ($quantity.length) {
                quantity= $quantity.val();
            }
        } else if ($this.hasClass('xmas-unclaim')) {
            url = '/unclaim';
            // TODO: Change the method to DELETE.
            // method = 'DELETE';
        } else if ($this.hasClass('xmas-purchase')) {
            url = '/purchase';
            method = 'PUT';
        } else if ($this.hasClass('xmas-return')) {
            url = '/return';
            method = 'PUT';
        }

        $.ajax({
            url: url,
            type: method,
            data: {id: id, quantity: quantity}
        }).done(function(html) {
            if ($this.hasClass('xmas-unclaim') && $this.closest('.xmas-section').hasClass('xmas-claims')) {
                $this.closest('.xmas-item').fadeOut('slow');
            } else {
                $this.closest('.xmas-item').replaceWith(html);
            }
        });
    });

    $('.xmas-wishlist').on('click', 'button', function(e) {
        var $this = $(this);
        var $item = $this.closest('.xmas-item');

        if ($this.hasClass('btn-add')) {
            return;
        }

        if ($this.hasClass('btn-cancel')) {
            $item.find('form').remove();
            $item.find('.btn-group').show();
            return;
        }

        e.preventDefault();

        var url = $this.closest('.xmas-wishlist').find('form').attr('action');
        url += '/' + $this.data('id');

        var method = '', data = {}, callback = null;
        if ($this.hasClass('btn-edit')) {
            method = 'GET';
            callback = function(html) {
                $item.find('.btn-group').hide();
                $item.append(html);
                initQuantity($item.find('input[name=quantity]'));
            };
        } else if ($this.hasClass('btn-update')) {
            method = 'PUT';
            data = $this.closest('form').serialize();
            callback = function(html) {
                if (html == 'OK') {
                    $item.find('form').remove();
                    $item.find('.btn-group').show();
                } else {
                    $item.html(html);
                }
            };
        } else if ($this.hasClass('btn-delete')) {
            if (!confirm('Are you sure you want to delete ' + $item.find('h3').html() + '?')) {
                return
            }
            method = 'DELETE';
            callback = function() {
                $item.parent().remove();
            }
        }

        $.ajax({
            url: url,
            type: method,
            data: data
        }).done(callback);
    });

    var initQuantity = function(this) {
        var $this = $(this);

        var id = $this.closest('form').find('input[name=id]').val();

        var $p = $('<p/>');
        $p.insertAfter($this.parent());

        var $label = $('<label for="qty-unlimited-' + id + '">Give me a lot!</label>');
        $p.append($label);

        var $check = $('<input type="checkbox" name="unlimited" id="qty-unlimited-' + id + '">');
        $p.append($check);

        $check.change(function() {
            if ($check.is(':checked')) {
                $check.data('original', $this.val());
                $this.hide();
                $this.val(0);
            } else {
                $this.val($check.data('original'));
                $this.show();
            }
        });

        if ($this.val() === '0') {
            $check.attr('checked', true);
            $check.change();
        }
    };

    $('.xmas-wishlist input[name=quantity]').each(function() {
        initQuantity(this);
    });
}(window.jQuery)
