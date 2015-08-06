var API_KEY;    // is changed later
var BODY;


window.addEventListener( 'load', function()
{
BODY = document.getElementById( 'ListBody' );

getAll();
});


function getAll()
{
$.post( '/v1/list/get_all', { api_key: API_KEY }, function( data )
    {
        // clear the table
    BODY.innerHTML = '';

    var posts = data[ 'post[]' ];

    for (var a = 0 ; a < posts.length ; a++)
        {
        var post = posts[ a ];
        var tr = document.createElement( 'tr' );
        var text = document.createElement( 'td' );
        var updated = document.createElement( 'td' );

        text.innerHTML = post.text;
        updated.innerHTML = post.last_updated;

        tr.appendChild( text );
        tr.appendChild( updated );

        BODY.appendChild( tr );
        }
    });
}