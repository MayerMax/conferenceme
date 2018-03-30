import { Component, OnInit } from '@angular/core';
import {FormBuilder, FormControl, FormGroup, Validators} from "@angular/forms";
import {Router} from "@angular/router";

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent implements OnInit {
  form: FormGroup;
  email = new FormControl('',[ Validators.required , Validators.email]);
  constructor(private fb: FormBuilder,private router: Router) {
  }
  getErrorMessage (){
    return this.email.hasError('required')? 'Вы должны ввести значение' :
      this.email.hasError('email')? "Недействительный адрес почты" : '';
  }
  login() {
    if (this.form.valid) {
      console.log('ok');
    }
  }
  ngOnInit() {
    this.form = this.fb.group(
      {
        password: ['', Validators.required]
      });
    this.form.addControl('email', this.email);
  }

}
