import { Injectable } from '@angular/core';
import {HttpClient} from "@angular/common/http";
import {Observable} from "rxjs/Observable";
import {Speaker} from "../constructor/models/speaker";

@Injectable()
export class GetDataService {
  private BaseUrl = 'http://localhost:8080/speaker/1';
  constructor(private  http: HttpClient) { }
 public getData(): Observable<Speaker> {
    let url = `${this.BaseUrl}`;
    return this.http.get<Speaker>(url);
  }

}
