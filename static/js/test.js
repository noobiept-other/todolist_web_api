var API_KEY;    // is changed later


window.addEventListener( 'load', function()
{
Test.init();
});


var Test;
(function(Test) {


var BODY;
var MESSAGE;
var ADD_DIALOG;
var UPDATE_DIALOG;
var REMOVE_DIALOG;
var TEXT_MAX_LENGTH = 0;


Test.init = function()
{
BODY = document.getElementById( 'ListBody' );
MESSAGE = document.getElementById( 'TestMessage' );


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
                    addPost( document.getElementById( 'AddText' ).value );

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


    // update dialog
UPDATE_DIALOG = document.getElementById( 'UpdateDialog' );

$( UPDATE_DIALOG ).dialog({
        autoOpen: false,
        modal: true,
        minWidth: 450,
        buttons: [
            {
                text: 'Update',
                click: function()
                    {
                    updatePost( $( UPDATE_DIALOG ).data( 'row' ), document.getElementById( 'UpdateText' ).value );

                    $( UPDATE_DIALOG ).dialog( 'close' );
                    }
            },
            {
                text: 'Cancel',
                click: function()
                    {
                    $( UPDATE_DIALOG ).dialog( 'close' );
                    }
            }
        ]
    });


    // remove dialog
REMOVE_DIALOG = document.getElementById( 'RemoveDialog' );

$( REMOVE_DIALOG ).dialog({
        autoOpen: false,
        modal: true,
        minWidth: 450,
        buttons: [
            {
                text: 'Remove',
                click: function()
                    {
                    deletePost( $( REMOVE_DIALOG ).data( 'row' ) );

                    $( REMOVE_DIALOG ).dialog( 'close' );
                    }
            },
            {
                text: 'Cancel',
                click: function()
                    {
                    $( REMOVE_DIALOG ).dialog( 'close' );
                    }
            }
        ]
    });


    // get the maximum length of the text
getInfo();
};


/**
 * Get some information about the list (maximum length of the text).
 * Show the list after.
 */
function getInfo( callback )
{
showLoadingMessage();

$.ajax({
        method: 'POST',
        url: '/v1/list/info',
        data: { api_key: API_KEY },
        success: function( data )
            {
            TEXT_MAX_LENGTH = data[ 'text_max_length' ];

                // update the 'add' and 'update' dialog input elements
            document.getElementById( 'AddText' ).setAttribute( 'maxlength', TEXT_MAX_LENGTH );
            document.getElementById( 'UpdateText' ).setAttribute( 'maxlength', TEXT_MAX_LENGTH );

                // load the list
            getAll();
            hideMessage();
            },
        error: function( jqXHR, textStatus, errorThrown )
            {
            console.log( textStatus, errorThrown );
            showErrorMessage();
            }
    });
}


/**
 * Get all the posts and add them to the table.
 */
function getAll()
{
showLoadingMessage();

$.ajax({
    method: 'POST',
    url: '/v1/list/get_all',
    data: { api_key: API_KEY },
    success: function( data )
        {
            // clear the table
        BODY.innerHTML = '';

        var posts = data[ 'post[]' ];

        for (var a = 0 ; a < posts.length ; a++)
            {
            addToTable( posts[ a ] );
            }

        hideMessage();
        },
    error: function( jqXHR, textStatus, errorThrown )
        {
        console.log( textStatus, errorThrown );
        showErrorMessage();
        }
    });
}


/**
 * Open the add dialog, used to add a new post to the list.
 */
function openAddDialog()
{
    // clear the text from previous calls
document.getElementById( 'AddText' ).value = '';

    // remove the focus off the button, otherwise when the dialog is closed it will set the focus to the button
$( '#Add' ).blur();

$( ADD_DIALOG ).dialog( 'open' );
}


/**
 * Open the update text dialog.
 */
function openUpdateDialog( row )
{
    // update the text input with the current text of the post
document.getElementById( 'UpdateText' ).value = row.firstElementChild.innerHTML;

    // save a reference to the row (we'll need it later on to update the table with the changes)
$( UPDATE_DIALOG ).data( 'row', row );
$( UPDATE_DIALOG ).dialog( 'open' );
}


/**
 * Open the remove post dialog.
 */
function openRemoveDialog( row )
{
    // show the text of the post to be removed
document.getElementById( 'RemoveText' ).innerHTML = row.firstElementChild.innerHTML;

$( REMOVE_DIALOG ).data( 'row', row );
$( REMOVE_DIALOG ).dialog( 'open' );
}


/**
 * Add a new post to the list via the list's api.
 * Update the table with the new post, if its successful.
 */
function addPost( text )
{
showLoadingMessage();

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
            addToTable( data, true );
            hideMessage();
            },
        error: function( jqXHR, textStatus, errorThrown )
            {
            console.log( textStatus, errorThrown );
            showErrorMessage();
            }
    });
}


/**
 * Update the text of an existing post.
 */
function updatePost( row, text )
{
showLoadingMessage();

$.ajax({
        method: 'POST',
        url: '/v1/list/update',
        data: {
            api_key: API_KEY,
            text: text,
            id: row.getAttribute( 'data-id' )
        },
        success: function( data, textStatus, jqXHR )
            {
            updateTableRow( data, row );
            hideMessage();
            },
        error: function( jqXHR, textStatus, errorThrown )
            {
            console.log( textStatus, errorThrown );
            showErrorMessage();
            }
    });
}


/**
 * Delete the selected post from the list/table.
 */
function deletePost( row )
{
showLoadingMessage();

$.ajax({
        method: 'POST',
        url: '/v1/list/delete',
        data: {
            api_key: API_KEY,
            id: row.getAttribute( 'data-id' )
        },
        success: function( data, textStatus, jqXHR )
            {
            removeTableRow( row );
            hideMessage();
            },
        error: function( jqXHR, textStatus, errorThrown )
            {
            console.log( textStatus, errorThrown );
            showErrorMessage();
            }
    });
}


/**
 * Add a new row to the table, based on a post information.
 */
function addToTable( info, inBeginning )
{
if ( typeof inBeginning === 'undefined' )
    {
    inBeginning = false;
    }

var tr = document.createElement( 'tr' );
var text = document.createElement( 'td' );
var updated = document.createElement( 'td' );
var controls = document.createElement( 'td' );
var updateButton = document.createElement( 'span' );
var removeButton = document.createElement( 'span' );

tr.setAttribute( 'data-id', info.id );

text.innerHTML = info.text;
updated.innerHTML = info.last_updated;
updateButton.title = 'Update Text';
removeButton.title = 'Remove Post';

$( updateButton ).button({
    text: false,
    icons: { primary: 'ui-icon-document-b' }
});
$( removeButton ).button({
    text: false,
    icons: { primary: 'ui-icon-close' }
});

updateButton.addEventListener( 'click', function()
    {
    openUpdateDialog( tr );
    });
removeButton.addEventListener( 'click', function()
    {
    openRemoveDialog( tr );
    });


controls.appendChild( updateButton );
controls.appendChild( removeButton );
tr.appendChild( text );
tr.appendChild( updated );
tr.appendChild( controls );

if ( inBeginning )
    {
    BODY.insertBefore( tr, BODY.firstElementChild );
    }

else
    {
    BODY.appendChild( tr );
    }
}


/**
 * Update a table row with the new information.
 */
function updateTableRow( info, row )
{
var text = row.firstElementChild;
var lastUpdated = text.nextElementSibling;

text.innerHTML = info.text;
lastUpdated.innerHTML = info.last_updated;
}


/**
 * Remove a table row.
 */
function removeTableRow( row )
{
row.parentNode.removeChild( row );
}


/**
 * Show a loading message.
 */
function showLoadingMessage()
{
MESSAGE.innerHTML = 'Loading..';
}


/**
 * Show an error message.
 */
function showErrorMessage()
{
MESSAGE.innerHTML = 'Error!';
}


/**
 * Hide the message element.
 */
function hideMessage()
{
MESSAGE.innerHTML = '';
}


})(Test || (Test = {}));






