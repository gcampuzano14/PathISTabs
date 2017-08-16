/*
This file contains all of the code running in the background.
These are HTML strings. In the main module, replace the %data% placeholder text you see in them.
*/

var comment_box = '<div class="thumbnail" id= "thumbnail_%comment_id%"><div class="caption" id="capt_div_%comment_id%"> \
	<div class = "form-inline"> <input type="checkbox" class = "comment_checkbox" id= "checkbox_%the_gene%_-_%condition%_-_%var%_-_%comment_id%" aria-label="..." style = "display:inline-block" %checked%> &nbsp;&nbsp;&nbsp;<h3 id= "heading_%comment_id%" style = "display:inline-block">%comment%</h3>\
	<div class="tab-content" style="display: inline-block; text-align: left; float: right"><button type="button" class="btn btn-warning edition_btn_%condition%_%var%" id="edit_%comment_id%"   data-toggle="tooltip" data-placement="top" title="Edit comment"><span class="glyphicon glyphicon-wrench"></span></button><br><br> </div></div><br>  \
	<textarea disabled="True" class="form-control" id="note_%comment_id%" name="comments" style = "resize: vertical; word-wrap: break-word; overflow: hidden">%comment_text%</textarea> \
	<br><span class="glyphicons glyphicons-keys"><h5>References</h5><div id = refs_list_%comment_id%>%references%</div> \
	</div></div>';


var new_comment_box = '<div class="thumbnail" id= "thumbnail_%comment_id%"><div class="caption" id="capt_div_%comment_id%"> \
	<div class = "form-inline"> <input type="checkbox" class = "comment_checkbox" id= "checkbox_%the_gene%_-_%condition%_-_%var%_-_%comment_id%" aria-label="..." style = "display:inline-block" %checked%> &nbsp;&nbsp;&nbsp; \
	<input type="text" value= "%the_heading%" class="form-control" size="50" style = "display:inline-block" id = "heading_%comment_id%" ></input> \
	<div class="tab-content" style="display: inline-block; text-align: left; float: right"> \
	<button class="btn btn-success saveeditbtn"  style = "display:inline-block"  data-toggle="tooltip" data-placement="top" title= "Save comment" id = "save_edit_%comment_id%"><span class="glyphicon glyphicon-floppy-saved"></span></button> \
	<button class="btn btn-default discard_edit"  style="display: inline-block; text-align: left; float: right"  data-toggle="tooltip" data-placement="top" title= "Discard changes and go back" id = "undo_edit_%comment_id%"><span class="glyphicon glyphicon-floppy-remove"></span></button><br style = "display:inline"> \
	<button class="btn btn-danger delete_comment"  style="display: inline-block;  float: right"  data-toggle="tooltip" data-placement="top" title= "Eliminate comment (permanent)" id = "erase_btn_%comment_id%"><span class="glyphicon glyphicon-trash"></span></button> \
	<br><br> </div></div><br> \
	<textarea class="form-control" id="note_%comment_id%" name="comments" style = "resize: vertical; word-wrap: break-word; overflow: hidden">%comment_text%</textarea> \
	<br><span class="glyphicons glyphicons-keys"><h5>References</h5><div id = refs_list_%comment_id%>%references%</div> \
	</div></div>';

var reference_elem = "<div id='a_ref_%ref_id%_%comment_id%'><a href = '%the_url%' target='_blank' class = 'the_refs_%comment_id%' id='a_ref_%ref_id%_%comment_id%' style = 'display:inline'>%citation%</a> \
		<button class='btn btn-link %comment_id%' id='ref_x_%ref_id%%comment_id%' style = 'display:inline'><span class='glyphicon glyphicon-remove' style = 'display:inline-block'></span></button><br><br></div>"

var ref_edit = '<div> \
	<div style="display: inline-block; vertical-align:top;"> \
	<button type="button" class="btn btn-primary pmid_btn" id="pmid_ref_btn_%comment_id%" style="display: inline-block;" data-toggle="tooltip" data-placement="top" title="Add reference via PMID">PMID \
	<span class="glyphicon glyphicon-ok"></span></button> \
	<input type="text" class="form-control" size="5" id="pmid_ref_str_%comment_id%" size="15" style = "display:inline-block" placeholder="PMID"></input>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; \
	</div> \
	<div style="display: inline-block;"> \
	<button type="button" class="btn btn-primary manual_ref" id="manual_ref_btn_%comment_id%"   data-toggle="tooltip" data-placement="top" title="Add reference via PMID"> \
	Manual entry&nbsp;&nbsp;&nbsp;<span class="glyphicon glyphicon-ok"></span></button>&nbsp;&nbsp;&nbsp; \
	<input type="text" class="form-control" id = "manual_title_%comment_id%" size="30" placeholder="Reference name or designator"></input> \
	<input type="text" class="form-control" id = "manual_citation_%comment_id%" size="30" placeholder="Reference as it will appear in the report"></input> \
	<input type="text" class="form-control" id = "manual_url_%comment_id%" size="30" placeholder="URL"></input></div></div>'

var refs_modal = '<div class="modal fade" id="myModal" tabindex="-1" role="dialog" aria-labelledby="myModalLabel"> \
	<div class="modal-dialog" role="document"><div class="modal-content">\
	<div class="modal-header">\
	<button type="button" class="close" data-dismiss="modal" aria-label="Close">\
	<span aria-hidden="true">&times;</span></button>\
	<h4 class="modal-title" id="myModalLabel">REFERENCE MANAGER</h4>\
	</div>\
	<div class="modal-body">\
	 <div class="input_fields_wrap">\
		<button class="add_field_button">Add More Fields</button>\
		<div><input type="text" name="mytext[]"></div>\
		</div>\
	<div class="modal-footer">\
	<button type="button" class="btn btn-default" data-dismiss="modal">Close</button>\
	<button type="button" class="btn btn-primary">Save changes</button>\
	</div>\
	</div>\
	</div>\
	</div>\
	</div>';

var warning_modal = '<div class="modal fade" id="myModal" tabindex="-1" role="dialog" aria-labelledby="myModalLabel"> \
	<div class="modal-dialog" role="document"><div class="modal-content">\
	<div class="modal-header">\
	<button type="button" class="close" data-dismiss="modal" aria-label="Close">\
	<span aria-hidden="true">&times;</span></button>\
	<h4 class="modal-title" id="myModalLabel">REFERENCE MANAGER</h4>\
	</div>\
	<div class="modal-body">\
	 <div class="input_fields_wrap">\
		<button class="add_field_button">Add More Fields</button>\
		<div><input type="text" name="mytext[]"></div>\
		</div>\
	<div class="modal-footer">\
	<button type="button" class="btn btn-default" data-dismiss="modal">Close</button>\
	<button type="button" class="btn btn-primary">Save changes</button>\
	</div>\
	</div>\
	</div>\
	</div>\
	</div>';

draggable_thumbnails = '<div class="thumbnail form-inline" id="%long_id%"><p style="color:red; display:inline-block">%gene%</p> \
	<div class="tab-content" style="display: inline-block; text-align: left; float: right"> \
	<button class="btn btn-link" id="" style = "display:inline"><span class="glyphicon glyphicon-remove" style = "display:inline-block"></span></button></div> \
	<p style="display: inline-block;">%condition%&nbsp;&nbsp;&nbsp;%variant% &nbsp;&nbsp;&nbsp;%comment%</p></div>'

var floating_ball = function floating_balls(){
var width = 1960,
    height = 1500;

var nodes = d3.range(500).map(function() { return {radius: Math.random() * 5 + 4}; }),
    root = nodes[0],
    color = d3.scale.category10();

root.radius = 0;
root.fixed = true;

var force = d3.layout.force()
    .gravity(0.01)
    .charge(function(d, i) { return i ? 0 : 2000; })
    .nodes(nodes)
    .size([width, height]);

force.start();

var svg = d3.select("body").append("svg")
    .attr("width", width)
    .attr("height", height);

svg.selectAll("circle")
    .data(nodes.slice(1))
  .enter().append("circle")
    .attr("r", function(d) { return d.radius; })
    .style("fill", function(d, i) { return color(i % 15); });

force.on("tick", function(e) {
  var q = d3.geom.quadtree(nodes),
      i = 0,
      n = nodes.length;

  while (++i < n) q.visit(collide(nodes[i]));

  svg.selectAll("circle")
      .attr("cx", function(d) { return d.x; })
      .attr("cy", function(d) { return d.y; });
});

svg.on("mousemove", function() {
  var p1 = d3.mouse(this);
  root.px = p1[0];
  root.py = p1[1];
  force.resume();
});

function collide(node) {
  var r = node.radius + 16,
      nx1 = node.x - r,
      nx2 = node.x + r,
      ny1 = node.y - r,
      ny2 = node.y + r;
  return function(quad, x1, y1, x2, y2) {
    if (quad.point && (quad.point !== node)) {
      var x = node.x - quad.point.x,
          y = node.y - quad.point.y,
          l = Math.sqrt(x * x + y * y),
          r = node.radius + quad.point.radius;
      if (l < r) {
        l = (l - r) / l * .5;
        node.x -= x *= l;
        node.y -= y *= l;
        quad.point.x += x;
        quad.point.y += y;
      }
    }
    return x1 > nx2 || x2 < nx1 || y1 > ny2 || y2 < ny1;
  };
}

}
