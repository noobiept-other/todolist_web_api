var API_KEY;    // is changed later


window.addEventListener( 'load', function()
{
Test.init();
});


var Test;
(function(Test) {


var BODY;
var ADD_DIALOG;


Test.init = function()
{
BODY = document.getElementById( 'ListBody' );


    // add post button/dialog
ADD_DIALOG = document.getElementById( 'AddDialog' );
var addButton = document.getElementById( 'Add' );

$( ADD_DIALOG ).dialog({
        autoOpen: false,
        modal: true,
        minWidth: 450,
        buttons: [
            {
                text: 'Add',
                click: function()
                    {
                    add( document.getElementById( 'AddText' ).value );

                    $( ADD_DIALOG ).dialog( 'close' );
                    }
            },
            {
                text: 'Cancel',
                click: function()
                    {
                    $( ADD_DIALOG ).dialog( 'close' );
                    }
            }
        ]
    });
$( addButton ).button();
addButton.addEventListener( 'click', openAddDialog );


    // show the list on start
getAll();
};


function getAll()
{
$.post( '/v1/list/get_all', { api_key: API_KEY }, function( data )
    {
        // clear the table
    BODY.innerHTML = '';

    var posts = data[ 'post[]' ];

    for (var a = 0 ; a < posts.length ; a++)
        {
        addToTable( posts[ a ] );
        }
    });
}


function openAddDialog()
{
$( ADD_DIALOG ).dialog( 'open' );
}


function add( text )
{
$.ajax({
        method: 'POST',
        url: '/v1/list/add',
        data: {
            api_key: API_KEY,
            text: text
        },
        dataType: 'json',
        success: function( data, textStatus, jqXHR )
            {
            addToTable( data );
            },
        error: function( jqXHR, textStatus, errorThrown )
            {
            console.log( textStatus, errorThrown );
            }
    });
}


function addToTable( info )
{
var tr = document.createElement( 'tr' );
var text = document.createElement( 'td' );
var updated = document.createElement( 'td' );

text.innerHTML = info.text;
updated.innerHTML = info.last_updated;

tr.appendChild( text );
tr.appendChild( updated );

BODY.appendChild( tr );
}


})(Test || (Test = {}));






