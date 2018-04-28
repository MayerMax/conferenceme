import {Directive, ElementRef, Input, OnChanges, Renderer, SimpleChange} from '@angular/core';

@Directive({
  selector: '[appImagePreview]'
})
export class ImagePreviewDirective {
  @Input() media: any ;
  @Input()type: any ;
  constructor(private el: ElementRef, private renderer: Renderer) { }
  ngOnChanges(changes) {
    console.log(changes);
    let reader = new FileReader();
    let el = this.el;
    if (this.type === 'application/pdf') {
      reader.onloadend = function (e) {
        el.nativeElement.data = reader.result;
      };
    } else if (this.type === 'image') {
      reader.onloadend = function (e) {
        el.nativeElement.src = reader.result;
      };
    }
    if (this.media) {
      return reader.readAsDataURL(this.media);
    }
  }
}
