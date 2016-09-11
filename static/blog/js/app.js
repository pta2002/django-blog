function reply(commentId) {
    $("#" + commentId + " > .panel-footer .reply-form").removeClass("hidden");
    $("#" + commentId + " > .panel-footer .reply").addClass("hidden");
}

function cancelreply(commentId) {
    $("#" + commentId + " > .panel-footer .reply-form").addClass("hidden");
    $("#" + commentId + " > .panel-footer .reply").removeClass("hidden");
}