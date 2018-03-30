import {Attribute, Directive} from '@angular/core';
import {FormControl, NG_VALIDATORS, Validator} from "@angular/forms";

@Directive({
  selector: '[compareFormControl]',
  providers: [{provide: NG_VALIDATORS,useExisting: CompareFormControlDirective, multi: true}]
})
export class CompareFormControlDirective implements Validator{

  constructor(@Attribute('compareFormControl') public comparer: string) { }
  validate(c: FormControl): {[key: string]: any}{
    let e = c.root.get(this.comparer);
    if(e && c.value !== e.value){
      return{"compare": true};
    }
    return null;
  }

}
